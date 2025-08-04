import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# The API code is assumed to be in a file named `main.py` in the same directory.
# If your file is named differently, update the import statement accordingly.
from Capstone.main import app, get_db, Base, User

# --- Test Database Setup ---
# Use an in-memory SQLite database for isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Recommended for SQLite in-memory with TestClient
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Dependency Override ---
# This function will override the `get_db` dependency in the main application
# to use our in-memory test database instead of the production one.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# --- Pytest Fixtures ---
# Fixtures provide a fixed baseline upon which tests can reliably and repeatedly execute.

@pytest.fixture(scope="function")
def db_session():
    """
    Pytest fixture to create a new database session for each test function.
    It creates all tables before the test runs and drops them afterwards,
    ensuring a clean slate for every test and complete test isolation.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Pytest fixture to provide a TestClient instance for making API requests.
    This fixture depends on `db_session` to ensure the database is
    initialized and cleaned up for each test.
    """
    # The `with` statement ensures that startup and shutdown events are run.
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Pytest fixture to create and commit a standard user to the database.
    This is useful for tests that require a pre-existing user.
    """
    user = User(name="Test User")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# --- Test Suites ---

class TestUserEndpoints:
    """Tests for the /users endpoints."""

    def test_create_user_happy_path(self, client, db_session):
        """Test creating a new user successfully."""
        response = client.post("/users", json={"name": "Alice"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert "id" in data

        # Verify the user exists in the database
        user_in_db = db_session.query(User).filter(User.id == data["id"]).first()
        assert user_in_db is not None
        assert user_in_db.name == "Alice"

    def test_create_user_invalid_payload(self, client):
        """Test user creation fails with an invalid JSON payload (missing 'name')."""
        response = client.post("/users", json={"username": "invalid"})
        assert response.status_code == 422  # Unprocessable Entity

    def test_get_user_by_id_happy_path(self, client):
        """Test retrieving an existing user by their ID."""
        # First, create a user to fetch
        create_response = client.post("/users", json={"name": "Bob"})
        user_id = create_response.json()["id"]

        # Now, fetch the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Bob"

    def test_get_user_not_found(self, client):
        """Test retrieving a user with an ID that does not exist."""
        response = client.get("/users/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_get_all_users_empty(self, client):
        """Test retrieving all users when the database is empty."""
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_users_populated(self, client):
        """Test retrieving all users when multiple users exist."""
        client.post("/users", json={"name": "Charlie"})
        client.post("/users", json={"name": "Dana"})

        response = client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Charlie"
        assert data[1]["name"] == "Dana"


class TestAffirmationMessageEndpoints:
    """Tests for the /messages endpoints."""

    def test_create_affirmation_happy_path(self, client, test_user):
        """Test creating an affirmation successfully for an existing user."""
        affirmation_data = {
            "user_id": test_user.id,
            "message": "You are capable of amazing things.",
            "category": "Self-worth",
            "date": "2023-10-27"
        }
        response = client.post("/messages", json=affirmation_data)
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == test_user.id
        assert data["message"] == "You are capable of amazing things."
        assert data["category"] == "Self-worth"
        assert data["date"] == "2023-10-27"
        assert "id" in data

    def test_create_affirmation_no_category(self, client, test_user):
        """Test creating an affirmation without the optional category field."""
        affirmation_data = {
            "user_id": test_user.id,
            "message": "Today is a new day.",
            "date": "2023-10-28"
        }
        response = client.post("/messages", json=affirmation_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Today is a new day."
        assert data["category"] is None

    def test_create_affirmation_user_not_found(self, client):
        """Test creating an affirmation fails for a non-existent user."""
        affirmation_data = {
            "user_id": 9999,
            "message": "This should fail.",
            "date": "2023-10-27"
        }
        response = client.post("/messages", json=affirmation_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_create_affirmation_invalid_payload(self, client, test_user):
        """Test creating an affirmation fails with missing required fields."""
        # Missing 'message'
        invalid_data = {"user_id": test_user.id, "date": "2023-10-27"}
        response = client.post("/messages", json=invalid_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_get_affirmation_by_id_happy_path(self, client, test_user):
        """Test retrieving an existing affirmation by its ID."""
        # First, create an affirmation to fetch
        affirmation_data = {
            "user_id": test_user.id,
            "message": "You've got this!",
            "date": "2023-10-27"
        }
        create_response = client.post("/messages", json=affirmation_data)
        affirmation_id = create_response.json()["id"]

        # Now, fetch it
        response = client.get(f"/messages/{affirmation_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == affirmation_id
        assert data["message"] == "You've got this!"
        assert data["user_id"] == test_user.id

    def test_get_affirmation_not_found(self, client):
        """Test retrieving an affirmation with an ID that does not exist."""
        response = client.get("/messages/9999")
        assert response.status_code == 404
        assert response.json() == {"detail": "Affirmation not found"}

    def test_get_all_affirmations_empty(self, client):
        """Test retrieving all affirmations when none exist."""
        response = client.get("/messages")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_affirmations_populated(self, client, test_user):
        """Test retrieving all affirmations when multiple exist."""
        client.post("/messages", json={
            "user_id": test_user.id,
            "message": "First message",
            "date": "2023-01-01"
        })
        client.post("/messages", json={
            "user_id": test_user.id,
            "message": "Second message",
            "category": "Positivity",
            "date": "2023-01-02"
        })

        response = client.get("/messages")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["message"] == "First message"
        assert data[1]["message"] == "Second message"
        assert data[1]["category"] == "Positivity"
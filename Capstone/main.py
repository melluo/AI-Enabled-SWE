from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, Session

app = FastAPI()
Base = declarative_base()

# CORS setup
origins = [
        "http://localhost:3000", # The address of your React frontend
        "localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    affirmations = relationship("AffirmationMessage", back_populates="user")

class AffirmationMessage(Base):
    __tablename__ = 'affirmation_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    category = Column(String)
    date = Column(String, nullable=False)
    user = relationship("User", back_populates="affirmations")

# Pydantic schemas
class UserCreate(BaseModel):
    name: str

class UserRead(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class AffirmationCreate(BaseModel):
    user_id: int
    message: str
    category: str = None
    date: str

class AffirmationRead(BaseModel):
    id: int
    user_id: int
    message: str
    category: str = None
    date: str
    class Config:
        orm_mode = True

# DB setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./affirmation.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create user
@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get all users
@app.get("/users", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Get user by id
@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create affirmation
@app.post("/messages", response_model=AffirmationRead)
def create_affirmation(affirmation: AffirmationCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == affirmation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_affirmation = AffirmationMessage(
        user_id=affirmation.user_id,
        message=affirmation.message,
        category=affirmation.category,
        date=affirmation.date
    )
    db.add(db_affirmation)
    db.commit()
    db.refresh(db_affirmation)
    return db_affirmation

# Get all affirmations
@app.get("/messages", response_model=List[AffirmationRead])
def get_affirmations(db: Session = Depends(get_db)):
    return db.query(AffirmationMessage).all()

# Get affirmation by id
@app.get("/messages/{affirmation_id}", response_model=AffirmationRead)
def get_affirmation(affirmation_id: int, db: Session = Depends(get_db)):
    affirmation = db.query(AffirmationMessage).filter(AffirmationMessage.id == affirmation_id).first()
    if not affirmation:
        raise HTTPException(status_code=404, detail="Affirmation not found")
    
# Delete user
@app.delete("/users/{user_id}", response_model=UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
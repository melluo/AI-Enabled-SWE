from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

# Pydantic models
class UserCreate(BaseModel):
    name: str

class UserRead(BaseModel):
    id: int
    name: str

class AffirmationCreate(BaseModel):
    message: str
    date: date
    category: Optional[str]
    user_id: int

class AffirmationRead(BaseModel):
    id: int
    message: str
    date: date
    category: Optional[str]
    user_id: int

# In-memory "database"
users_db = []
affirmations_db = []

# CRUD Endpoints for Users
@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    new_id = len(users_db) + 1
    new_user = {"id": new_id, "name": user.name}
    users_db.append(new_user)
    return new_user

@app.get("/users", response_model=List[UserRead])
def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# CRUD Endpoints for Affirmations
@app.post("/messages", response_model=AffirmationRead)
def create_affirmation(affirmation: AffirmationCreate):
    # Check if user exists
    user_exists = any(user["id"] == affirmation.user_id for user in users_db)
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_id = len(affirmations_db) + 1
    new_affirmation = {
        "id": new_id,
        "message": affirmation.message,
        "date": affirmation.date,
        "category": affirmation.category,
        "user_id": affirmation.user_id
    }
    affirmations_db.append(new_affirmation)
    return new_affirmation

@app.get("/messages", response_model=List[AffirmationRead])
def get_affirmations():
    return affirmations_db

@app.get("/messages/{message_id}", response_model=AffirmationRead)
def get_affirmation(message_id: int):
    for affirmation in affirmations_db:
        if affirmation["id"] == message_id:
            return affirmation
    raise HTTPException(status_code=404, detail="Affirmation not found")
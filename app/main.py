from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import UserCRUD
from app.tenant import get_db
from app.database import db_manager
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

app = FastAPI(title="Multi-tenant FastAPI Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db_manager.initialize()

@app.on_event("shutdown")
async def shutdown():
    await db_manager.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return await UserCRUD.create_user(db, username=user.username, email=user.email)

@app.get("/users/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return await UserCRUD.get_users(db, skip=skip, limit=limit)

@app.get("/users/{username}", response_model=UserResponse)
async def get_user(
    username: str,
    db: Session = Depends(get_db)
):
    user = await UserCRUD.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
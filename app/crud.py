from sqlalchemy.orm import Session
from app.models import User
from typing import List, Optional

class UserCRUD:
    @staticmethod
    async def create_user(db: Session, username: str, email: str) -> User:
        db_user = User(username=username, email=email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
    @staticmethod
    async def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
        
    @staticmethod
    async def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
        
    @staticmethod
    async def update_user(
        db: Session,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None
    ) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            if username:
                user.username = username
            if email:
                user.email = email
            db.commit()
            db.refresh(user)
        return user
        
    @staticmethod
    async def delete_user(db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
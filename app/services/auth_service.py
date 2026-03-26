from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import verify_password, hash_password
from typing import Optional
from pydantic import EmailStr

# namespace for related auth methods
class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def authenticate_user(db: Session, email: EmailStr, password: str) -> Optional[User]:
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_password = hash_password(user.password)
        db_user = User(
            email=user.email,
            first_name=user.first_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        # save to the db:
        db.commit()
        # sync object from db with Python so that its aware of db-generated values like id.
        db.refresh(db_user)
        return db_user

    @staticmethod
    def is_email_taken(db: Session, email: EmailStr) -> bool:
        return db.query(User).filter(User.email == email).first() is not None


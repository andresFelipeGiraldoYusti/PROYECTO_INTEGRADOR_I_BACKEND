from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext

from app.models.users import Users

from app.repositories.user_repository import UsersRepository
from app.schemas.users_schema import UsersCreate, UsersUpdate

from app.security.hash_manager import hash_password


class UsersService:

    @staticmethod
    def create_user(db: Session, user: UsersCreate):
        existing_user = UsersRepository.get_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already registered")
        user.password_hash = hash_password(user.password_hash)

        return UsersRepository.create(db, user)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return UsersRepository.get_by_id(db, user_id)
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return UsersRepository.get_by_email(db, email)
    
    @staticmethod
    def get_all_users(db: Session):
        return UsersRepository.get_all(db)
    
    @staticmethod
    def update_user(db: Session, user: UsersUpdate):
        db_user = UsersService.get_user_by_email(db, user.email)
        if not db_user:
            raise ValueError("User not found")
        
        db_user.full_name = user.full_name
        db_user.rol = user.rol
        db_user.phone_number = user.phone_number
        db_user.password_hash = hash_password(user.password_hash)
        db_user.update_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        return UsersRepository.update_user(db, db_user)

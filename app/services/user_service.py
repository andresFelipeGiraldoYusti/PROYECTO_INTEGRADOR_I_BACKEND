from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repositories.user_repository import UsersRepository
from app.schemas.users_schema import UsersCreate

from app.security.hash_manager import hash_password


class UsersService:

    @staticmethod
    def create_user(db: Session, user: UsersCreate):
        existing_user = UsersRepository.get_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already registered")

        print(user.password_hash)
        user.password_hash = hash_password(user.password_hash)

        return UsersRepository.create(db, user)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return UsersRepository.get_by_id(db, user_id)

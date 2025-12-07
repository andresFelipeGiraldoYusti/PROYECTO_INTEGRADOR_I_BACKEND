from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.users import Users

from app.repositories.user_repository import UsersRepository
from app.schemas.users_schema import UsersCreate, UsersRead

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
    
    @staticmethod
    def get_all_users(db: Session):
        return UsersRepository.get_all(db)
    
    @staticmethod
    def update_user(db: Session, user: UsersRead):
        db_user = db.query(Users).get(user.id)
        if not db_user:
            raise ValueError("User not found")

        db_user.email = user.email
        db_user.full_name = user.full_name
        db_user.rol = user.rol

        return UsersRepository.update_user(db, db_user)

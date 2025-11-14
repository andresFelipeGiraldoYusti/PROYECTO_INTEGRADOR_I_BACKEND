from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repositories.user_repository import UsersRepository
from app.schemas.users_schema import UsersCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsersService:

    @staticmethod
    def create_user(db: Session, user: UsersCreate):
        # Verificar si el email ya existe
        existing_user = UsersRepository.get_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already registered")

        # Hashear contraseña
        hashed_password = pwd_context.hash(user.password)

        # Crear usuario en la DB
        return UsersRepository.create(db, user.username, user.email, hashed_password)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return UsersRepository.get_by_id(db, user_id)

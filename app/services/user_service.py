from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Verificar si el email ya existe
        existing_user = UserRepository.get_by_email(db, user.email)
        if existing_user:
            raise ValueError("Email already registered")

        # Hashear contraseña
        hashed_password = pwd_context.hash(user.password)

        # Crear usuario en la DB
        return UserRepository.create(db, user.username, user.email, hashed_password)

    @staticmethod
    def get_user(db: Session, user_id: int):
        return UserRepository.get_by_id(db, user_id)

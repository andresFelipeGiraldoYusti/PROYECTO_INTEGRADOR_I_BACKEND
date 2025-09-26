from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    @staticmethod
    def create(db: Session, username: str, email: str, password: str) -> User:
        db_user = User(username=username, email=email, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

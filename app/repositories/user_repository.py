from sqlalchemy.orm import Session
from app.models.users import Users

class UsersRepository:

    @staticmethod
    def create(db: Session, Usersname: str, email: str, password: str) -> Users:
        db_Users = Users(Usersname=Usersname, email=email, password=password)
        db.add(db_Users)
        db.commit()
        db.refresh(db_Users)
        return db_Users

    @staticmethod
    def get_by_id(db: Session, Users_id: int) -> Users:
        return db.query(Users).filter(Users.id == Users_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Users:
        return db.query(Users).filter(Users.email == email).first()

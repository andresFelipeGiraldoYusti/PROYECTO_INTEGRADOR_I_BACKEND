from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.users_schema import UsersCreate

class UsersRepository:

    @staticmethod
    def create(db: Session, user: UsersCreate) -> Users:
        data = user.model_dump(exclude={"id", "create_at", "update_at"})
        db_user = Users(**data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_by_id(db: Session, Users_id: int) -> Users:
        return db.query(Users).filter(Users.id == Users_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Users:
        return db.query(Users).filter(Users.email == email).first()
    
    @staticmethod
    def get_all(db: Session) -> list[Users]:
        return db.query(Users).all()
    
    @staticmethod
    def update_user(db: Session, user: Users) -> Users:
        print(user)
        db.merge(user)
        db.commit()
        db.refresh(user)
        return user

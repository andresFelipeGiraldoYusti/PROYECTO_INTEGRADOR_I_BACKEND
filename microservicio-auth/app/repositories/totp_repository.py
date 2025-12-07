from sqlalchemy.orm import Session
from app.models.totp import TOTP
from app.schemas.totp_schema import TOTPCreate

class TOTPRepository:
    @staticmethod
    def create_totp_secret(db: Session, user: TOTPCreate) -> TOTP:
        data =user.model_dump(exclude={"id", "create_at", "update_at"})
        db_totp = TOTP(**data)
        db.add(db_totp)
        db.commit()
        db.refresh(db_totp)
        return db_totp
    
    @staticmethod
    def get_totp_by_user_id(db: Session, user_id: int) -> TOTP:
        return db.query(TOTP).filter(TOTP.user_id == user_id).first()
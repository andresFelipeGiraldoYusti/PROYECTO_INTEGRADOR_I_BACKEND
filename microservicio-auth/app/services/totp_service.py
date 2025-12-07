from app.security.totp_manager import generate_totp_secret, generate_totp_qr_uri, verify_totp_secret
from app.repositories.totp_repository import TOTPRepository
from app.schemas.totp_schema import TOTPCreate
from sqlalchemy.orm import Session
from app.core.config import settings
from datetime import datetime

class TOTPService:
    @staticmethod
    def get_totp_by_user_id(id: int):
        return TOTPRepository.get_totp_by_user_id(id)
    
    @staticmethod
    def generate_totp_secret(db: Session, id: int):
        key_totp = generate_totp_qr_uri(str(id), settings.NAME_PROJECT)
        existing_user = TOTPRepository.get_totp_by_user_id(db, id)
        print(f"Usuario existente: {existing_user}")
        if existing_user:
            raise ValueError("Este usuario ya ha generado una clave TOTP")
        totp_data = TOTPCreate(
            user_id=id,
            secret_key=key_totp['secret'],
            is_active=True,
            created_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            update_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        db_totp = TOTPRepository.create_totp_secret(db, totp_data)

        return {
            "message": "Clave TOTP generada correctamente",
            "totp_qr": key_totp['qr_code'],
        }
        
    @staticmethod
    def verify_totp_code(db: Session, id: int, totp_code: str):
        totp_record = TOTPRepository.get_totp_by_user_id(db, id)
        print(f"clave secreta: {totp_record.secret_key}")
        if not totp_record:
            raise ValueError("No se encontró una clave TOTP para este usuario")
        if not totp_record.is_active:
            raise ValueError("La clave TOTP para este usuario no está activa")
        is_valid = verify_totp_secret(totp_code, totp_record.secret_key)
        
        return {
            "message": "Código TOTP verificado correctamente",
            "is_valid": is_valid['is_valid']
        }
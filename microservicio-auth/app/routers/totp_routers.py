from fastapi import APIRouter, Depends

from app.services.totp_service import TOTPService
from app.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.security.totp_manager import generate_totp_secret, generate_totp_qr_uri

router = APIRouter(prefix="/totp", tags=["TOTP"])

@router.post("/generate_totp")
async def generate_totp(db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        return TOTPService.generate_totp_secret(db, user.id)
    except ValueError as e:
        return {"error": str(e)}
    
@router.post("/verify_totp")
async def verify_totp(db: Session = Depends(get_db), user = Depends(get_current_user), totp_code: str = ""):
    try:
        return TOTPService.verify_totp_code(db, user.id, totp_code)
    except ValueError as e:
        return {"error": str(e)}
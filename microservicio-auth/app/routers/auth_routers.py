from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
import pyotp
import time

from app.security.hash_manager import hash_password, verify_password
from app.security.totp_manager import generate_totp_secret, verify_totp_secret, generate_totp_qr_uri

from app.services.suppliers_service import SuppliersService
from app.schemas.suppliers_schema import SupplierCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/generar_contraseña_hash")
def hash(password: str, db: Session = Depends(get_db)):
    try:
        return hash_password(password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/verificar_hash")
def verify(password: str, hash: str, db: Session = Depends(get_db)):
    try:
        is_valid = verify_password(password, hash)
        return {"is_valid": is_valid}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/generate_totp_secret")
def generate_totp():
    try:
        return generate_totp_secret()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/generate_totp_qr_uri")
def generate_totp_qr(username: str, issuer_name: str, db: Session = Depends(get_db)):
    try:
        return generate_totp_qr_uri(username, issuer_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/verify_totp")
def verify_totp(token: str, secret: str,  db: Session = Depends(get_db)):
    try:
        print(token, secret)
        return verify_totp_secret(token, secret)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.security.hash_manager import hash_password, verify_password

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
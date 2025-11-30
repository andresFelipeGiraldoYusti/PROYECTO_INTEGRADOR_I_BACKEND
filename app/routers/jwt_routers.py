from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.security.jwt_manager import create_jwt_token, verify_jwt_token

router = APIRouter()

router = APIRouter(prefix="/jwt", tags=["JWT"])

@router.post("/generar_token")
def generar_token(user_id: int, username: str, db: Session = Depends(get_db)):
    try:
        token = create_jwt_token(user_id=user_id, username=username)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user_id,
            "username": username
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar token: {str(e)}")
    

@router.post("/verificar_token")
def verificar_token(token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_jwt_token(token)
        return {
            "valido": True,
            "user_id": payload["sub"],
            "username": payload["username"],
            "expiracion": payload["exp"]
        }
    except HTTPException as e:
        return {
            "valido": False,
            "error": e.detail
        }
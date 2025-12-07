from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.schemas.users_schema import UsersCreate
from app.services.user_service import UsersService
from app.auth.login import authenticate
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password
    try:
        token = authenticate(db, email, password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/register")
def register_user(user: UsersCreate, 
                  db: Session = Depends(get_db),
                  admin_user = Depends(require_admin)
                  ):
    try:
        db_user = UsersService.create_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

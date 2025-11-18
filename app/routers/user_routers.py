from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.schemas.users_schema import UsersCreate, UsersRead
from app.services.user_service import UsersService
from app.auth.login import authenticate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create_user", response_model=UsersCreate)
def create_user(user: UsersCreate, db: Session = Depends(get_db)):
    try:
        db_user = UsersService.create_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UsersRead)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UsersRead:
    db_user = UsersService.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/autentucar/{username}/{password}", response_model=UsersRead)
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)) -> UsersRead:
    db_user = authenticate(db, username, password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return db_user


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/create_user", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = UserService.create_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

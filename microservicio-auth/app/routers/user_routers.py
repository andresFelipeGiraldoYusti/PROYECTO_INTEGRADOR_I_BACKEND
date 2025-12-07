from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.auth.dependencies import require_admin
from app.schemas.users_schema import UsersRead
from app.services.user_service import UsersService
from app.auth.login import authenticate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UsersRead)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UsersRead:
    db_user = UsersService.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/get_all_users")
def create_user(db: Session = Depends(get_db), admin_user = Depends(require_admin)):
    try:
        db_user = UsersService.get_all_users(db)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/update_user")
def update_user(user: UsersRead,
                db: Session = Depends(get_db),
                admin_user = Depends(require_admin)
                ):
    try:
        db_user = UsersService.update_user(db, user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

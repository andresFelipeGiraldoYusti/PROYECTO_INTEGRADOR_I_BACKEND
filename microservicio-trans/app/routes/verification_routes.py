# app/routes/verification_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.verification_schema import VerificationResponse
from app.controllers.verification_controller import verify_transaction_controller
from app.schemas.verification_schema import TransactionVerificationRequest

router = APIRouter()

@router.post("/transactions", response_model=VerificationResponse)
def verify_transaction_endpoint(
    data: TransactionVerificationRequest,
    db: Session = Depends(get_db),
):
    return verify_transaction_controller(data, db)

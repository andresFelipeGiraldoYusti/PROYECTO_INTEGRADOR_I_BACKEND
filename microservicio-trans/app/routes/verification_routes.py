# app/routes/verification_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.verification_schema import VerificationResponse
from controllers.verification_controller import verify_transaction_controller
from schemas.verification_schema import TransactionVerificationRequest
from security.jwt_dependency import require_user

router = APIRouter(dependencies=[Depends(require_user)])

@router.post("/transactions", response_model=VerificationResponse)
def verify_transaction_endpoint(
    data: TransactionVerificationRequest,
    db: Session = Depends(get_db),
):
    return verify_transaction_controller(data, db)

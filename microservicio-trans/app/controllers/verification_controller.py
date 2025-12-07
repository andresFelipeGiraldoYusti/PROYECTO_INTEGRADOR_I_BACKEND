# app/controllers/verification_controller.py
from sqlalchemy.orm import Session
from schemas.verification import TransactionVerificationRequest, VerificationResponse
from services.verification_service import create_and_verify_transaction

def verify_transaction_controller(
    data: TransactionVerificationRequest,
    db: Session,
) -> VerificationResponse:
    tx, estado, detalles = create_and_verify_transaction(db, data)

    return VerificationResponse(
        transaction_id=tx.id,
        estado_verificacion=estado,
        verification_status=tx.verification_status.value,
        mfa_status=tx.mfa_status.value,
        detalles=detalles or [],
    )

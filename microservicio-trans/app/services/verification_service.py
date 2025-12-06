# app/services/verification_service.py
from sqlalchemy.orm import Session
from models.transactions import Transactions, VerificationStatus, MFAStatus
from services.validation_service import validate_purchase_order
from services.risk_engine import should_require_mfa
from services.mfa_service import send_mfa_challenge
from schemas.verification import TransactionVerificationRequest

def create_and_verify_transaction(db: Session, data: TransactionVerificationRequest):
    # 1) Crear la transacción en la base de datos
    tx = Transactions(
        user_id=data.user_id,
        supplier_id=data.supplier_id,
        product_type=data.product_type,
        amount=data.amount,
        verification_status=VerificationStatus.PENDING,
        mfa_status=MFAStatus.NOT_REQUIRED,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    # 2) Validaciones RF-06 (datos de proveedor / orden)
    errores, alertas = validate_purchase_order(db, tx)
    detalles = errores + alertas

    if errores:
        # Si hay errores críticos, la verificación falla y no se pide MFA
        tx.verification_status = VerificationStatus.FAILED
        tx.mfa_status = MFAStatus.NOT_REQUIRED
    else:
        # 3) RF-01: políticas de riesgo → decidir si requiere MFA
        requiere_mfa = should_require_mfa(db, tx)

        if requiere_mfa:
            tx.verification_status = VerificationStatus.NEEDS_ADDITIONAL_CHECKS
            tx.mfa_status = MFAStatus.PENDING
            # RF-05: contexto de transacción + creación de sesión MFA
            send_mfa_challenge(db, tx)
        else:
            tx.verification_status = VerificationStatus.SUCCESS
            tx.mfa_status = MFAStatus.NOT_REQUIRED

    tx.verification_details = "\n".join(detalles) if detalles else None
    db.commit()
    db.refresh(tx)

    # 4) Traducción al texto que espera el sistema origen
    if tx.verification_status == VerificationStatus.FAILED:
        estado = "verificación fallida"
    elif tx.mfa_status == MFAStatus.PENDING:
        estado = "requiere verificaciones adicionales"
        # (porque está pendiente de que el usuario apruebe el MFA)
    else:
        estado = "verificación exitosa"

    return tx, estado, detalles

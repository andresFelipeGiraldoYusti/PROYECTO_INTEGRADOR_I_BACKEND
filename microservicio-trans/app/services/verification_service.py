# app/services/verification_service.py
from sqlalchemy.orm import Session
from typing import List

from models.transactions import Transactions, VerificationStatus, MFAStatus
from services.validation_service import (
    validate_purchase_order,
    validate_supplier_payload_against_db,
)
from services.risk_engine import should_require_mfa
from schemas.verification_schema import TransactionVerificationRequest
from models.roles import Roles
from services.external_user_service import get_user_by_id


def user_has_risk_override(db: Session, user: dict | None) -> bool:
    """
    Devuelve True si el rol del usuario está configurado en BD
    para poder saltarse políticas de riesgo y MFA.
    Ahora `user` es un dict obtenido desde el servicio externo.
    """
    if not user:
        return False

    role_id = user.get("role_id")
    if not role_id:
        return False

    role = db.query(Roles).filter(Roles.id == role_id).first()
    if not role:
        return False

    return bool(role.can_override_risk)


def create_and_verify_transaction(db: Session, data: TransactionVerificationRequest):
    # Usuario obtenido desde servicio externo (mock por ahora)
    user = get_user_by_id(data.user_id)

    tx = Transactions(
        user_id=data.user_id,
        supplier_id=data.supplier_id,
        product_type_id=data.product_type_id,
        amount=data.amount,
        verification_status=VerificationStatus.PENDING,
        mfa_status=MFAStatus.NOT_REQUIRED,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    errores_totales: List[str] = []
    alertas_totales: List[str] = []

    # 1) Validaciones de consistencia entre payload y BD
    errores_payload, alertas_payload = validate_supplier_payload_against_db(db, data)
    errores_totales.extend(errores_payload)
    alertas_totales.extend(alertas_payload)

    # 2) Validaciones de la orden de compra / proveedor / RUES
    errores_orden, alertas_orden = validate_purchase_order(db, tx)
    errores_totales.extend(errores_orden)
    alertas_totales.extend(alertas_orden)

    # 3) Si hay errores duros, se marca como fallida
    if errores_totales:
        tx.verification_status = VerificationStatus.FAILED
        tx.mfa_status = MFAStatus.NOT_REQUIRED

    else:
        # 4) Ver si el usuario tiene permiso para saltarse políticas de riesgo
        if user_has_risk_override(db, user):
            tx.verification_status = VerificationStatus.SUCCESS
            tx.mfa_status = MFAStatus.NOT_REQUIRED
        else:
            # 5) Motor de riesgo decide si requiere MFA
            requiere_mfa = should_require_mfa(db, tx)

            if requiere_mfa:
                tx.verification_status = VerificationStatus.NEEDS_ADDITIONAL_CHECKS
                tx.mfa_status = MFAStatus.PENDING

                alertas_totales.append(
                    "La transacción requiere verificación MFA según políticas de riesgo."
                )
                
            else:
                tx.verification_status = VerificationStatus.SUCCESS
                tx.mfa_status = MFAStatus.NOT_REQUIRED

    # 6) Construir detalle final (errores + alertas) y guardar en la transacción
    detalles = errores_totales + alertas_totales
    tx.verification_details = "\n".join(detalles) if detalles else None

    db.commit()
    db.refresh(tx)

    # 7) Texto legible para el estado
    if tx.verification_status == VerificationStatus.FAILED:
        estado = "verificación fallida"
    elif tx.mfa_status == MFAStatus.PENDING:
        estado = "requiere verificaciones adicionales"
    else:
        estado = "verificación exitosa"

    return tx, estado, detalles

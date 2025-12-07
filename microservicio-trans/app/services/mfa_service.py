# app/services/mfa_service.py
from sqlalchemy.orm import Session
from datetime import datetime
from models.transactions import Transactions
from models.suppliers import Suppliers
from models.mfa_devices import MFADevices
from models.mfa_session import MFASession

def build_mfa_message(db: Session, tx: Transactions) -> str:
    supplier = db.query(Suppliers).filter(Suppliers.id == tx.supplier_id).first()
    supplier_name = supplier.comercial_name or supplier.legal_name if supplier else "Proveedor"
    amount = tx.amount
    return f"¿Está autorizando una orden para {supplier_name} por un monto de {amount} COP?"


def get_primary_mfa_device(db: Session, user_id: int) -> MFADevices | None:
    device = (
        db.query(MFADevices)
        .filter(
            MFADevices.user_id == user_id,
            MFADevices.is_primary == True,
            MFADevices.is_verified == True,
        )
        .first()
    )
    return device


def create_mfa_session(db: Session, tx: Transactions, device: MFADevices) -> MFASession:
    session = MFASession(
        transaction_id=tx.id,
        mfa_device_id=device.id,
        created_at=datetime.now(),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def send_mfa_challenge(db: Session, tx: Transactions) -> str:
    device = get_primary_mfa_device(db, tx.user_id)
    if not device:
        # aquí puedes lanzar excepción o fallback
        raise RuntimeError("Usuario sin dispositivo MFA registrado/verificado")

    message = build_mfa_message(db, tx)

    # TODO: integración real (SMS, email, push, TOTP, etc.)
    print(f"[MFA] Enviando a user {tx.user_id} / device {device.id}: {message}")

    session = create_mfa_session(db, tx, device)
    return str(session.id)  # usamos el id de MFASession como referencia

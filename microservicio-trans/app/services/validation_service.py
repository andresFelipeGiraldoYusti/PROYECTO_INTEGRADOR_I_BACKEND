# app/services/validation_service.py
from typing import List, Tuple
from sqlalchemy.orm import Session

from models.transactions import Transactions
from models.suppliers import Suppliers
from schemas.verification_schema import TransactionVerificationRequest
from services.external import rues_validation


def validate_purchase_order(db: Session, tx: Transactions) -> Tuple[List[str], List[str]]:
    """
    Valida que la orden de compra tenga un proveedor válido y que
    la información mínima del proveedor esté consistente y activa en RUES.
    Esta validación aplica SIEMPRE, sin importar el rol (ni siquiera el CEO se la salta).
    """
    errores: List[str] = []
    alertas: List[str] = []

    supplier = db.query(Suppliers).filter(Suppliers.id == tx.supplier_id).first()
    if not supplier:
        errores.append("Proveedor no encontrado en la base de datos")
        return errores, alertas

    if not supplier.legal_name:
        errores.append("Nombre legal del proveedor vacío")

    if not supplier.nit:
        errores.append("NIT del proveedor vacío")
        
    if not supplier.comercial_name:
        errores.append("Nombre comercial del proveedor vacío")

    # Validación contra RUES u otra fuente externa
    status = rues_validation.get_rues_status(supplier.nit)
    if status == "INACTIVO":
        errores.append("Cámara de comercio del proveedor aparece inactiva")

    return errores, alertas


def validate_supplier_payload_against_db(
    db: Session, data: TransactionVerificationRequest
) -> Tuple[List[str], List[str]]:
    """
    Compara los datos del proveedor enviados por el sistema origen
    (legal_name, nit, comercial_name) contra lo registrado en BD
    para el supplier_id indicado en la transacción.
    """
    errores: List[str] = []
    alertas: List[str] = []

    supplier = (
        db.query(Suppliers)
        .filter(Suppliers.id == data.supplier_id)
        .first()
    )

    if not supplier:
        errores.append(
            "Proveedor no encontrado en la base de datos para el supplier_id enviado"
        )
        return errores, alertas

    # Comparar NIT
    if supplier.nit != data.nit:
        errores.append(
            "El NIT enviado no coincide con el NIT registrado en la base de datos"
        )

    # Comparar nombre legal
    if supplier.legal_name != data.legal_name:
        errores.append(
            "El nombre legal enviado no coincide con el registrado en la base de datos"
        )

    # Comparar nombre comercial
    if data.comercial_name:
        if supplier.comercial_name is None:
            alertas.append(
                "El proveedor en BD no tiene nombre comercial, pero el request sí envía uno"
            )
        elif supplier.comercial_name != data.comercial_name:
            alertas.append(
                "El nombre comercial enviado no coincide con el registrado en la base de datos"
            )

    return errores, alertas

# app/services/validation_service.py
from typing import List, Tuple
from sqlalchemy.orm import Session
from models.transactions import Transactions
from models.suppliers import Suppliers
from services.external import rues_validation

def validate_purchase_order(db: Session, tx: Transactions) -> Tuple[List[str], List[str]]:
    errores: List[str] = []
    alertas: List[str] = []

    supplier = db.query(Suppliers).filter(Suppliers.id == tx.supplier_id).first()
    if not supplier:
        errores.append("Proveedor no encontrado")
        return errores, alertas

    if not supplier.legal_name:
        errores.append("Nombre legal del proveedor vacío")

    if not supplier.nit:
        errores.append("NIT del proveedor vacío")
        
    if not supplier.comercial_name:
        errores.append("Nombre comercial del proveedor vacío")
    
    if not supplier.risk_category in ["LOW", "MEDIUM", "HIGH"]:
        alertas.append("Categoría de riesgo del proveedor no está definida correctamente")
    
    status= rues_validation.get_rues_status(supplier.nit)
    if status == "INACTIVO":
        errores.append("Cámara de comercio del proveedor aparece inactiva")
    
    return errores, alertas

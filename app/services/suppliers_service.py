from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repositories.suppliers_repository import SuppliersRepository
from app.schemas.suppliers_schema import SupplierCreate

class SuppliersService:

    @staticmethod
    def create_supplier(db: Session, supplier: SupplierCreate):
        # Verificar si el NIT ya existe
        existing_supplier = SuppliersRepository.get_by_nit(db, supplier.nit)
        if existing_supplier:
            raise ValueError("NIT already registered")

        # Crear proveedor en la DB
        return SuppliersRepository.create(
            db,
            nit=supplier.nit,
            legal_name=supplier.legal_name,
            comercial_name=supplier.comercial_name,
            risk_category=supplier.risk_category
        )

    @staticmethod
    def get_supplier(db: Session, supplier_id: int):
        return SuppliersRepository.get_by_id(db, supplier_id)
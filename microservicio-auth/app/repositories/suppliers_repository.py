from sqlalchemy.orm import Session
from app.models.suppliers import Suppliers

class SuppliersRepository:

    @staticmethod
    def create(db: Session, nit: str, legal_name: str, comercial_name: str = None, risk_category: str = "MEDIUM") -> Suppliers:
        db_supplier = Suppliers(nit=nit, legal_name=legal_name, comercial_name=comercial_name, risk_category=risk_category)
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier

    @staticmethod
    def get_by_id(db: Session, supplier_id: int) -> Suppliers:
        return db.query(Suppliers).filter(Suppliers.id == supplier_id).first()

    @staticmethod
    def get_by_nit(db: Session, nit: str) -> Suppliers:
        return db.query(Suppliers).filter(Suppliers.nit == nit).first()
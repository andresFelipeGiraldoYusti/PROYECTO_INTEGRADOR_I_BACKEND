from sqlalchemy.orm import Session
from app.models.suppliers import Suppliers
from app.schemas.supplier_schema import SupplierCreate


def create_supplier(db: Session, data: SupplierCreate) -> Suppliers:
    supplier = Suppliers(
        nit=data.nit,
        legal_name=data.legal_name,
        comercial_name=data.comercial_name,
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def get_supplier(db: Session, supplier_id: int) -> Suppliers | None:
    return db.query(Suppliers).filter(Suppliers.id == supplier_id).first()


def get_all_suppliers(db: Session) -> list[Suppliers]:
    return db.query(Suppliers).all()


def search_suppliers(
    db: Session,
    supplier_id: int | None = None,
    nit: str | None = None,
    legal_name: str | None = None,
    comercial_name: str | None = None,
) -> list[Suppliers]:
    q = db.query(Suppliers)

    if supplier_id is not None:
        q = q.filter(Suppliers.id == supplier_id)

    if nit:
        q = q.filter(Suppliers.nit == nit)

    if legal_name:
        q = q.filter(Suppliers.legal_name.ilike(f"%{legal_name}%"))

    if comercial_name:
        q = q.filter(Suppliers.comercial_name.ilike(f"%{comercial_name}%"))

    return q.all()


def update_supplier(db: Session, supplier_id: int, data: SupplierCreate) -> Suppliers | None:
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return None

    supplier.nit = data.nit
    supplier.legal_name = data.legal_name
    supplier.comercial_name = data.comercial_name

    db.commit()
    db.refresh(supplier)
    return supplier


def delete_supplier(db: Session, supplier_id: int) -> bool:
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        return False
    db.delete(supplier)
    db.commit()
    return True

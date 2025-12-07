from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db

from schemas.supplier_schema import SupplierCreate, SupplierResponse
from services.supplier_service import (
    create_supplier, search_suppliers, get_supplier,
    update_supplier, delete_supplier,
)

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.post("/", response_model=SupplierResponse)
def create_supplier_endpoint(data: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(db, data)


@router.get("/", response_model=list[SupplierResponse])
def list_or_search_suppliers(
    supplier_id: int | None = None,
    nit: str | None = None,
    legal_name: str | None = None,
    comercial_name: str | None = None,
    db: Session = Depends(get_db),
):
    suppliers = search_suppliers(
        db,
        supplier_id=supplier_id,
        nit=nit,
        legal_name=legal_name,
        comercial_name=comercial_name,
    )
    return suppliers


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier_by_id(supplier_id: int, db: Session = Depends(get_db)):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(404, "Proveedor no encontrado")
    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier_endpoint(
    supplier_id: int,
    data: SupplierCreate,
    db: Session = Depends(get_db),
):
    updated = update_supplier(db, supplier_id, data)
    if not updated:
        raise HTTPException(404, "Proveedor no encontrado")
    return updated


@router.delete("/{supplier_id}")
def delete_supplier_endpoint(supplier_id: int, db: Session = Depends(get_db)):
    ok = delete_supplier(db, supplier_id)
    if not ok:
        raise HTTPException(404, "Proveedor no encontrado")
    return {"message": "Proveedor eliminado"}

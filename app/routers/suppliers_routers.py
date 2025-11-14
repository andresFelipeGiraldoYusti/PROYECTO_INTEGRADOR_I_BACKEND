from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.services.suppliers_service import SuppliersService
from app.schemas.suppliers_schema import SupplierCreate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/create_supplier", response_model=SupplierCreate)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    try:
        db_supplier = SuppliersService.create_supplier(db, supplier)
        return db_supplier
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
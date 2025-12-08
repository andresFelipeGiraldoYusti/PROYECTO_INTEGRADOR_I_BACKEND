# app/routes/product_type_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.product_type_schema import ProductTypeCreate, ProductTypeResponse
from services.product_type_service import (
    create_product_type,
    search_product_types,
    get_product_type,
    update_product_type,
    delete_product_type,
)

# 👇 ESTA variable *debe* existir a nivel global
router = APIRouter(prefix="/product-types", tags=["product-types"])


@router.post("/", response_model=ProductTypeResponse)
def create_pt_endpoint(data: ProductTypeCreate, db: Session = Depends(get_db)):
    return create_product_type(db, data)


@router.get("/", response_model=list[ProductTypeResponse])
def list_or_search_pt(
    pt_id: int | None = None,
    name: str | None = None,
    db: Session = Depends(get_db),
):
    pts = search_product_types(db, pt_id=pt_id, name=name)
    return pts


@router.get("/{pt_id}", response_model=ProductTypeResponse)
def get_pt_endpoint(pt_id: int, db: Session = Depends(get_db)):
    pt = get_product_type(db, pt_id)
    if not pt:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return pt


@router.put("/{pt_id}", response_model=ProductTypeResponse)
def update_pt_endpoint(
    pt_id: int,
    data: ProductTypeCreate,
    db: Session = Depends(get_db),
):
    updated = update_product_type(db, pt_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return updated


@router.delete("/{pt_id}")
def delete_pt_endpoint(pt_id: int, db: Session = Depends(get_db)):
    ok = delete_product_type(db, pt_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return {"message": "Tipo de producto eliminado"}

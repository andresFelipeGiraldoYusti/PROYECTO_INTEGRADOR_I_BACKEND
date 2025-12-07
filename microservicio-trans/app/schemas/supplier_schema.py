# schemas/supplier_schema.py
from pydantic import BaseModel


class SupplierBase(BaseModel):
    nit: str
    legal_name: str
    comercial_name: str | None = None


class SupplierCreate(SupplierBase):
    """Datos usados para crear / actualizar un proveedor."""
    pass


class SupplierResponse(SupplierBase):
    id: int

    class Config:
        orm_mode = True

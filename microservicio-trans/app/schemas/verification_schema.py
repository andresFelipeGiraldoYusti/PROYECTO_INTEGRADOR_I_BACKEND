from pydantic import BaseModel, Field
from typing import List, Optional

class TransactionVerificationRequest(BaseModel):
    user_id: int = Field(..., description="ID del usuario que solicita la transacción")
    supplier_id: int = Field(..., description="ID del proveedor asociado")
    legal_name: str = Field(..., description="Nombre legal del proveedor (según sistema origen)")
    nit: str = Field(..., description="NIT del proveedor (según sistema origen)")
    comercial_name: Optional[str] = Field(
        None, description="Nombre comercial del proveedor (según sistema origen)"
    )
    product_type_id: int = Field(..., description="Tipo de producto involucrado")
    amount: int = Field(..., description="Monto total de la transacción en unidades enteras")

class VerificationResponse(BaseModel):
    transaction_id: int
    estado_verificacion: str
    verification_status: str
    mfa_status: str
    detalles: Optional[List[str]] = None

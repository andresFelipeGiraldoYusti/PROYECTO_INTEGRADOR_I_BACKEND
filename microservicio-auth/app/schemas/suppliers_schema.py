from pydantic import BaseModel, EmailStr

class SupplierCreate(BaseModel):
    nit: str
    legal_name: str
    comercial_name: str | None = None
    risk_category: str | None = "MEDIUM"
    
class SupplierRead(BaseModel):
    nit: str
    legal_name: str
    amount: str
    comercial_name: str | None = None
    risk_category: str | None = "MEDIUM"

    class Config:
        from_attributes = True
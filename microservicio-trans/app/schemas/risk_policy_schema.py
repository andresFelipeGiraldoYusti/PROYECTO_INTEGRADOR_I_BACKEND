from pydantic import BaseModel

class RiskPolicyBase(BaseModel):
    rol: str
    amount: int
    product_type_id: int
    supplier_id: int
    mfa_action: str

class RiskPolicyCreate(RiskPolicyBase):
    pass

class RiskPolicyResponse(RiskPolicyBase):
    id: int

    product_type_name: str | None = None
    supplier_name: str | None = None

    class Config:
        orm_mode = True

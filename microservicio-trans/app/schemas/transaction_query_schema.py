from pydantic import BaseModel
from datetime import datetime

class TransactionQueryResponse(BaseModel):
    id: int
    user_name: str
    supplier_name: str
    product_type_name: str | None
    amount: int
    verification_status: str
    mfa_status: str
    create_at: datetime | None = None

    class Config:
        orm_mode = True

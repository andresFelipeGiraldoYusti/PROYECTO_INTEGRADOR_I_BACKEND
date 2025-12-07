from pydantic import BaseModel

class TOTPCreate(BaseModel):
    user_id: int
    secret_key: str
    is_active: bool
    created_at: str
    update_at: str
    
    class Config:
        orm_mode = True
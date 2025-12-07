from pydantic import BaseModel, EmailStr

class UsersCreate(BaseModel):
    email: EmailStr
    full_name: str
    rol: str
    phone_number: str
    password_hash: str

class UsersRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    rol: str

    class Config:
        from_attributes = True
        orm_mode = True

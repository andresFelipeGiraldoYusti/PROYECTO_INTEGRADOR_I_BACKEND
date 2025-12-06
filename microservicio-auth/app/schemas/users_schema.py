from pydantic import BaseModel, EmailStr

class UsersCreate(BaseModel):
    email: EmailStr
    full_name: str
    dapartment: str
    phone_number: str
    username: str
    password_hash: str

class UsersRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

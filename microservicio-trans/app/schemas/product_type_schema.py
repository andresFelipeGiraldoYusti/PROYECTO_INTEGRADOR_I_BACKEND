from pydantic import BaseModel

class ProductTypeBase(BaseModel):
    name: str
    description: str | None = None

class ProductTypeCreate(ProductTypeBase):
    pass

class ProductTypeResponse(ProductTypeBase):
    id: int

    class Config:
        orm_mode = True

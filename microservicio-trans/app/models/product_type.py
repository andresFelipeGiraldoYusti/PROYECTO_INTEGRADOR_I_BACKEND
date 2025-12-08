# app/models/product_type.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.session import Base

class ProductTypes(Base):
    __tablename__ = "product_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

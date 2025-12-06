# app/models/supplier.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.session import Base

class Suppliers(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nit = Column(String(20), unique=True, nullable=False)
    legal_name = Column(String(200), nullable=False)
    comercial_name = Column(String(200))
    risk_category = Column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

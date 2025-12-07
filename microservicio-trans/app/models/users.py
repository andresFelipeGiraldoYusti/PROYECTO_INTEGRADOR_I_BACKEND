#/models/users.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.session import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    dapartment = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    create_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now())
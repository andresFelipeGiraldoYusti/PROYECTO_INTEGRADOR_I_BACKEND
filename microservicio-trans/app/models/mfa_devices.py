#/models/mfa_devices.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from db.session import Base

class MFADevices(Base):
    __tablename__ = "mfa_devices"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_type = Column(String(20), nullable=False)
    device_name = Column(String(100), nullable=False)
    secret_key = Column(String(255), nullable=False)
    public_key = Column(String(255))
    credential_id = Column(String(255))
    phone_number = Column(String(20))
    backup_codes = Column(String(500))
    is_primary = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    registered_at = Column(DateTime, default=datetime.now)
    last_used_at = Column(DateTime, default=datetime.now)
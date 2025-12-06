from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from db.session import Base

class TOTPConfigurations(Base):
    __tablename__ = "totp_configurations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("mfa_devices.id"), nullable=False)
    secret_key = Column(String(255), nullable=False)
    algorithm = Column(String(20), nullable=False)
    digits = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)
    backup_codes = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    last_used_at = Column(DateTime, default=datetime.now)
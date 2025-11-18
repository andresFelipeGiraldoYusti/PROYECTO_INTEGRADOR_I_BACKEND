from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from app.db.session import Base

class MFASession(Base):
    __tablename__ = "mfa_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False )
    mfa_device_id = Column(Integer, ForeignKey("mfa_devices.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
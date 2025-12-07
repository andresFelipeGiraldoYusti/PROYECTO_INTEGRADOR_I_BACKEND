# app/models/transaction.py
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum, Text
)
from datetime import datetime
from sqlalchemy.sql import func
import enum
from db.session import Base


class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    NEEDS_ADDITIONAL_CHECKS = "NEEDS_ADDITIONAL_CHECKS"


class MFAStatus(str, enum.Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Transactions(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # antes: product_type = Column(String(50), nullable=False)
    product_type_id = Column(Integer, ForeignKey("product_types.id"), nullable=True)

    amount = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    verification_status = Column(
        Enum(VerificationStatus),
        default=VerificationStatus.PENDING,
        nullable=False,
    )
    verification_details = Column(Text, nullable=True)

    mfa_status = Column(
        Enum(MFAStatus),
        default=MFAStatus.NOT_REQUIRED,
        nullable=False,
    )

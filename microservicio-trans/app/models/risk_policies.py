# app/models/risk_policy.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from db.session import Base

class RiskPolicies(Base):
    __tablename__ = "risk_policies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    policy_name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))

    amount = Column(Integer, nullable=False)  # umbral de monto

    # Por ahora string; después puedes migrar a FK product_type_id
    product_type = Column(String(50), nullable=False)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)

    # Ej: "REQUIRE_MFA", "SKIP_MFA", "ALWAYS_MFA"
    mfa_action = Column(String(20), nullable=False)

    is_active = Column(Boolean, default=True)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

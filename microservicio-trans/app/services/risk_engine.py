# app/services/risk_engine.py
from sqlalchemy.orm import Session

from app.models.transactions import Transactions
from app.models.risk_policies import RiskPolicies
from app.models.suppliers import Suppliers
from app.services.external_user_service import get_user_by_id

def get_policies_for_tx(db: Session, tx: Transactions) -> list[RiskPolicies]:
    user = get_user_by_id(tx.user_id)
    user_rol = user.rol if user else None
    return (
        db.query(RiskPolicies)
        .filter(
            RiskPolicies.is_active == True,
            RiskPolicies.supplier_id == tx.supplier_id,
            RiskPolicies.rol == user_rol,
            RiskPolicies.product_type_id == tx.product_type_id,
        )
        .order_by(RiskPolicies.amount.asc())
        .all()
    )


def choose_policy_by_range(policies: list[RiskPolicies], amount: int) -> RiskPolicies | None:
    if not policies:
        return None

    n = len(policies)

    for i, p in enumerate(policies):
        lower = p.amount
        upper = policies[i + 1].amount if i + 1 < n else None

        # Si amount es menor o igual a la política actual → usar esa
        if amount <= lower:
            return p

        # amount entre lower y upper
        if upper is not None and lower < amount <= upper:
            return p

        # amount mayor que la última política → aplicar la última
        if upper is None and amount > lower:
            return p

    return None


def should_require_mfa(db: Session, tx: Transactions) -> bool:
    """
    Aplica las políticas de riesgo para decidir si la transacción requiere MFA.
    """

    policies = get_policies_for_tx(db, tx)
    policy = choose_policy_by_range(policies, tx.amount)

    if policy:
        action = (policy.mfa_action or "").upper()

        if action in ("MFA"):
            return True
        if action in ("SKIP_MFA"):
            return False

        # Si la acción es desconocida, por seguridad, exigir MFA
        return True

    # Si no hay políticas específicas, se puede evaluar por categoría de riesgo del proveedor
    supplier = db.query(Suppliers).filter(Suppliers.id == tx.supplier_id).first()

    if not supplier:
        return True

    category = (getattr(supplier, "risk_category", "MEDIUM") or "MEDIUM").upper()

    if category == "HIGH":
        return True
    if category in ("MEDIUM", "LOW"):
        return False

    return True
# app/services/risk_engine.py
from sqlalchemy.orm import Session

from app.models.transactions import Transactions
from app.models.risk_policies import RiskPolicies
from app.models.suppliers import Suppliers
from app.services.external_user_service import get_user_by_id

def get_policies_for_tx(db: Session, tx: Transactions) -> list[RiskPolicies]:
    user = get_user_by_id(tx.user_id)
    user_rol = user["rol"] if user else None
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
    """
    Asume que `RiskPolicies.amount` es el límite superior (upper bound) de cada política.
    Las políticas vienen ordenadas ascendentemente por `amount`. 
    - Si amount <= límite de una política, se aplica esa política.
    - Si amount es mayor que el máximo límite disponible, NO se aplica ninguna (se devuelve None -> rechazo).
    """
    if not policies:
        return None

    for p in policies:
        if amount <= p.amount:
            return p

    # Si el monto es mayor que el mayor límite definido, no hay política aplicable
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
            return "REQUIRE_MFA"
        if action in ("SKIP_MFA"):
            return "NOT_REQUIRED"

        # Si la acción es desconocida, por seguridad, exigir MFA
        return "REQUIRE_MFA"

    # Si no hay políticas retornar que requiere MFA por defecto    
    return "REJECTED"
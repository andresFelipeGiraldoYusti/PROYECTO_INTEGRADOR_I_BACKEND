# app/services/risk_engine.py
from sqlalchemy.orm import Session

from models.transactions import Transactions
from models.risk_policies import RiskPolicies
from models.suppliers import Suppliers
from models.roles import Roles
from services.external_user_service import get_user_by_id


def user_can_override_mfa(db: Session, user_id: int) -> bool:
    """
    Determina si el usuario puede omitir las políticas de riesgo/MFA.
    El usuario se obtiene ahora desde un servicio externo (mock con user_data()).
    """
    user = get_user_by_id(user_id)
    if not user:
        return False

    role_id = user.get("role_id")
    if not role_id:
        return False

    role = db.query(Roles).filter(Roles.id == role_id).first()
    return bool(role and role.can_override_risk)


def get_policies_for_tx(db: Session, tx: Transactions) -> list[RiskPolicies]:
    return (
        db.query(RiskPolicies)
        .filter(
            RiskPolicies.is_active == True,
            RiskPolicies.supplier_id == tx.supplier_id,
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
    # Si el usuario tiene permiso para saltarse MFA, no se exige
    if user_can_override_mfa(db, tx.user_id):
        return False

    policies = get_policies_for_tx(db, tx)
    policy = choose_policy_by_range(policies, tx.amount)

    if policy:
        action = (policy.mfa_action or "").upper()

        if action in ("ALWAYS_MFA", "REQUIRE_MFA"):
            return "REQUIRE_MFA"
        if action in ("NEVER_MFA", "SKIP_MFA"):
            return "NOT_REQUIRED"

        # Si la acción es desconocida, por seguridad, exigir MFA
        return "REQUIRE_MFA"

    # Si no hay políticas retornar que requiere MFA por defecto    
    return "REJECTED"

from sqlalchemy.orm import Session
from models.transactions import Transactions
from models.risk_policies import RiskPolicies
from models.suppliers import Suppliers
from models.users import Users
from models.roles import Roles


def user_can_override_mfa(db: Session, user_id: int) -> bool:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user or not getattr(user, "role_id", None):
        return False

    role = db.query(Roles).filter(Roles.id == user.role_id).first()
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

    # Recorrer cada política ordenada
    for i, p in enumerate(policies):

        lower = p.amount
        upper = policies[i + 1].amount if i + 1 < n else None

        # Si amount es menor a la política → usar esa
        if amount <= lower:
            return p

        # Caso 1: amount entre lower y upper
        if upper is not None and lower < amount and amount <= upper:
            return p

        # Caso 2: amount mayor que la última política → aplicar la última
        if upper is None and amount > lower:
            return p

    return None



def should_require_mfa(db: Session, tx: Transactions) -> bool:
    if user_can_override_mfa(db, tx.user_id):
        return False

    policies = get_policies_for_tx(db, tx)
    policy = choose_policy_by_range(policies, tx.amount)

    if policy:
        action = (policy.mfa_action or "").upper()

        if action in ("ALWAYS_MFA", "REQUIRE_MFA"):
            return True
        if action in ("NEVER_MFA", "SKIP_MFA"):
            return False

        return True

    supplier = db.query(Suppliers).filter(Suppliers.id == tx.supplier_id).first()

    if not supplier:
        return True

    category = (supplier.risk_category or "MEDIUM").upper()

    if category == "HIGH":
        return True
    if category in ("MEDIUM", "LOW"):
        return False

    return True

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.risk_policies import RiskPolicies
from app.models.suppliers import Suppliers
from app.models.product_type import ProductTypes
from app.schemas.risk_policy_schema import RiskPolicyCreate


def create_risk_policy(db: Session, data: RiskPolicyCreate) -> RiskPolicies:
    policy = RiskPolicies(
        rol=data.rol,
        amount=data.amount,
        product_type_id=data.product_type_id,
        supplier_id=data.supplier_id,
        mfa_action=data.mfa_action,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def get_risk_policy(db: Session, policy_id: int) -> RiskPolicies | None:
    return db.query(RiskPolicies).filter(RiskPolicies.id == policy_id).first()


def search_risk_policies(
    db: Session,
    rol: str | None = None,
    supplier_name: str | None = None,
    supplier_id: int | None = None,
    mfa_action: str | None = None,
    product_type_name: str | None = None,
) -> list[RiskPolicies]:
    q = (
    db.query(
        RiskPolicies,
        Suppliers.legal_name.label("supplier_name"),
        ProductTypes.name.label("product_type_name")
        )
        .join(Suppliers, RiskPolicies.supplier_id == Suppliers.id)
        .join(ProductTypes, RiskPolicies.product_type_id == ProductTypes.id)
    )   

    if rol:
        q = q.filter(RiskPolicies.rol.ilike(f"%{rol}%"))

    if supplier_id is not None:
        q = q.filter(RiskPolicies.supplier_id == supplier_id)

    if supplier_name:
        q = q.filter(
            or_(
                Suppliers.legal_name.ilike(f"%{supplier_name}%"),
                Suppliers.comercial_name.ilike(f"%{supplier_name}%"),
            )
        )

    if mfa_action:
        q = q.filter(RiskPolicies.mfa_action.ilike(mfa_action.upper()))

    if product_type_name:
        q = q.filter(ProductTypes.name.ilike(f"%{product_type_name}%"))

    results = []
    for policy, supplier_name, product_type_name in q.all():
        results.append({
            "id": policy.id,
            "rol": policy.rol,
            "amount": policy.amount,
            "product_type_id": policy.product_type_id,
            "product_type_name": product_type_name,
            "supplier_id": policy.supplier_id,
            "supplier_name": supplier_name,
            "mfa_action": policy.mfa_action
        })

    return results


def update_risk_policy(db: Session, policy_id: int, data: RiskPolicyCreate) -> RiskPolicies | None:
    policy = get_risk_policy(db, policy_id)
    if not policy:
        return None

    policy.rol = data.rol
    policy.amount = data.amount
    policy.product_type_id = data.product_type_id
    policy.supplier_id = data.supplier_id
    policy.mfa_action = data.mfa_action

    db.commit()
    db.refresh(policy)
    return policy


def delete_risk_policy(db: Session, policy_id: int) -> bool:
    policy = get_risk_policy(db, policy_id)
    if not policy:
        return False
    db.delete(policy)
    db.commit()
    return True

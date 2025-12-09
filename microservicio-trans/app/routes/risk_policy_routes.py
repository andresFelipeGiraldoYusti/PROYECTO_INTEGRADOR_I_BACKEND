from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from security.jwt_dependency import require_user

from schemas.risk_policy_schema import RiskPolicyCreate, RiskPolicyResponse
from services.risk_policy_service import (
    create_risk_policy, get_risk_policy, search_risk_policies,
    update_risk_policy, delete_risk_policy,
)

router = APIRouter(dependencies=[Depends(require_user)], prefix="/risk-policies", tags=["risk-policies"])


@router.post("/", response_model=RiskPolicyResponse)
def create_policy_endpoint(data: RiskPolicyCreate, db: Session = Depends(get_db)):
    return create_risk_policy(db, data)


@router.get("/", response_model=list[RiskPolicyResponse])
def list_or_search_policies(
    rol: str | None = None,
    supplier_name: str | None = None,
    supplier_id: int | None = None,
    mfa_action: str | None = None,
    product_type_name: str | None = None,
    db: Session = Depends(get_db),
):
    policies = search_risk_policies(
        db,
        rol=rol,
        supplier_name=supplier_name,
        supplier_id=supplier_id,
        mfa_action=mfa_action,
        product_type_name=product_type_name,
    )
    return policies


@router.get("/{policy_id}", response_model=RiskPolicyResponse)
def get_policy_endpoint(policy_id: int, db: Session = Depends(get_db)):
    policy = get_risk_policy(db, policy_id)
    if not policy:
        raise HTTPException(404, "Política no encontrada")
    return policy


@router.put("/{policy_id}", response_model=RiskPolicyResponse)
def update_policy_endpoint(policy_id: int, data: RiskPolicyCreate, db: Session = Depends(get_db)):
    updated = update_risk_policy(db, policy_id, data)
    if not updated:
        raise HTTPException(404, "Política no encontrada")
    return updated


@router.delete("/{policy_id}")
def delete_policy_endpoint(policy_id: int, db: Session = Depends(get_db)):
    ok = delete_risk_policy(db, policy_id)
    if not ok:
        raise HTTPException(404, "Política no encontrada")
    return {"message": "Política eliminada"}

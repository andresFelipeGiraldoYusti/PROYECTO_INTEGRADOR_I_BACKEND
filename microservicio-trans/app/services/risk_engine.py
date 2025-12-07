# app/services/risk_engine.py
from sqlalchemy.orm import Session
from models.transactions import Transactions
from models.risk_policies import RiskPolicies
from models.suppliers import Suppliers

def get_applicable_policy(db: Session, tx: Transactions) -> RiskPolicies | None:
    # Trae todas las políticas activas para ese proveedor + tipo de producto
    policies = (
        db.query(RiskPolicies)
        .filter(
            RiskPolicies.is_active == True,
            RiskPolicies.supplier_id == tx.supplier_id,
            RiskPolicies.product_type == tx.product_type,
        )
        .order_by(RiskPolicies.amount.asc())  # ordena por umbral
        .all()
    )

    applicable = None
    for p in policies:
        # usamos la política cuyo amount sea <= monto de la transacción
        if tx.amount >= p.amount:
            applicable = p

    return applicable


def should_require_mfa(db: Session, tx: Transactions) -> bool:
    # 1) Primero: políticas configuradas por el admin
    policy = get_applicable_policy(db, tx)

    if policy:
        action = (policy.mfa_action or "").upper()

        if action == "ALWAYS_MFA":
            return True
        if action == "NEVER_MFA":
            return False
        if action == "REQUIRE_MFA":
            return True
        if action == "SKIP_MFA":
            return False

        # Acción desconocida → default seguro
        return True

    # 2) Si NO hay política en BD, decides una regla simple sin montos

    supplier = db.query(Suppliers).filter(Suppliers.id == tx.supplier_id).first()
    if not supplier:
        # Sin información del proveedor → MFA por seguridad
        return True

    cat = (supplier.risk_category or "MEDIUM").upper()

    # Aquí ya NO usamos montos, solo categoría.
    # Ejemplo de regla:
    if cat == "HIGH":
        return True          # siempre MFA para proveedores de alto riesgo
    if cat in ("MEDIUM", "LOW"):
        return False         # si no hay política, no pedimos MFA por monto

    # Fallback muy básico
    return True

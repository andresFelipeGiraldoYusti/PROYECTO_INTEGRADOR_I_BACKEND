# app/services/risk_engine.py
from sqlalchemy.orm import Session
from models.transactions import Transactions
from models.risk_policies import RiskPolicies
from models.suppliers import Suppliers  # por si luego quieres usar más criterios


def get_applicable_policy(db: Session, tx: Transactions) -> RiskPolicies | None:
    """
    Busca las políticas activas que aplican para:
      - ese proveedor
      - ese tipo de producto
    y se queda con la política cuyo 'amount' sea el mayor umbral
    que no supera el monto de la transacción.
    """

    policies = (
        db.query(RiskPolicies)
        .filter(
            RiskPolicies.is_active == True,
            RiskPolicies.supplier_id == tx.supplier_id,
            RiskPolicies.product_type_id == tx.product_type_id,
        )
        .order_by(RiskPolicies.amount.asc())
        .all()
    )

    applicable = None
    for p in policies:
        if tx.amount >= p.amount:
            applicable = p  # siempre termina con la de mayor amount <= tx.amount

    return applicable


def should_require_mfa(db: Session, tx: Transactions) -> bool:
    # 1) Intentar aplicar políticas de riesgo configuradas por el admin
    policy = get_applicable_policy(db, tx)

    if policy:
        action = (policy.mfa_action or "").upper()

        if action == "ALWAYS_MFA":
            return True          # siempre MFA
        if action == "REQUIRE_MFA":
            return True          # requiere MFA a partir de ese umbral
        if action == "NEVER_MFA":
            return False         # nunca MFA (por ejemplo, proveedores ultra confiables)
        if action == "SKIP_MFA":
            return False         # se omite MFA en ese rango

        # Acción desconocida → default seguro
        return True

    # 2) Si NO hay política configurada para ese proveedor + producto
    #    decides un criterio por defecto.
    #    Puedes ser estricto (True) o laxo (False).
    return True  # por seguridad, si no hay reglas, pedimos MFA

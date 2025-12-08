# app/services/transaction_query_service.py
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.transactions import Transactions
from models.suppliers import Suppliers
from models.product_type import ProductTypes
from services.external_user_service import get_user_by_id


def search_transactions(
    db: Session,
    user_name: str | None = None,        # nombre completo
    username: str | None = None,         # username de login
    supplier_name: str | None = None,
    product_type_name: str | None = None,
    amount_min: int | None = None,
    amount_max: int | None = None,
):
    """
    Ahora los datos del usuario no vienen de la tabla `users`,
    sino del servicio externo (mock user_data()).
    """
    q = (
        db.query(Transactions, Suppliers, ProductTypes)
        .join(Suppliers, Transactions.supplier_id == Suppliers.id)
        .join(ProductTypes, Transactions.product_type_id == ProductTypes.id, isouter=True)
    )

    if supplier_name:
        q = q.filter(
            or_(
                Suppliers.legal_name.ilike(f"%{supplier_name}%"),
                Suppliers.comercial_name.ilike(f"%{supplier_name}%"),
            )
        )

    if product_type_name:
        q = q.filter(ProductTypes.name.ilike(f"%{product_type_name}%"))

    if amount_min is not None:
        q = q.filter(Transactions.amount >= amount_min)

    if amount_max is not None:
        q = q.filter(Transactions.amount <= amount_max)

    # Traemos primero todas las filas que dependen solo de BD
    rows = q.all()

    results = []

    for tx, supplier, pt in rows:
        user = get_user_by_id(tx.user_id)

        # Filtros por usuario (se aplican en memoria porque vienen de servicio externo)
        if username:
            if not user or user.get("username") != username:
                continue

        if user_name:
            if not user or user_name.lower() not in user.get("full_name", "").lower():
                continue

        # Nombre del usuario para la respuesta
        if user:
            user_full_name = user.get("full_name", "Usuario sin nombre")
        else:
            user_full_name = "Usuario no encontrado"

        results.append(
            {
                "id": tx.id,
                "user_name": user_full_name,
                "supplier_name": supplier.comercial_name or supplier.legal_name,
                "product_type_name": pt.name if pt else None,
                "amount": tx.amount,
                "verification_status": tx.verification_status.value,
                "mfa_status": tx.mfa_status.value,
                "create_at": tx.create_at,
            }
        )

    return results

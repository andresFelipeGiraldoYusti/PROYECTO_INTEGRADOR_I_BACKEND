from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from models.transactions import Transactions
from models.users import Users
from models.suppliers import Suppliers
from models.product_type import ProductTypes


def search_transactions(
    db: Session,
    user_name: str | None = None,        # nombre completo
    username: str | None = None,         # username de login
    supplier_name: str | None = None,
    product_type_name: str | None = None,
    amount_min: int | None = None,
    amount_max: int | None = None,
):
    q = (
        db.query(Transactions, Users, Suppliers, ProductTypes)
        .join(Users, Transactions.user_id == Users.id)
        .join(Suppliers, Transactions.supplier_id == Suppliers.id)
        .join(ProductTypes, Transactions.product_type_id == ProductTypes.id, isouter=True)
    )

    if user_name:
        q = q.filter(Users.full_name.ilike(f"%{user_name}%"))

    if username:
        q = q.filter(Users.username == username)

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

    results = []
    for tx, user, supplier, pt in q.all():
        results.append(
            {
                "id": tx.id,
                "user_name": user.full_name,
                "supplier_name": supplier.comercial_name or supplier.legal_name,
                "product_type_name": pt.name if pt else None,
                "amount": tx.amount,
                "verification_status": tx.verification_status.value,
                "mfa_status": tx.mfa_status.value,
                "create_at": tx.create_at,
            }
        )

    return results

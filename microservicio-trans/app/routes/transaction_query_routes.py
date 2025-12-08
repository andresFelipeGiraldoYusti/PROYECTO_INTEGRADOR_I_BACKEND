from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db

from schemas.transaction_query_schema import TransactionQueryResponse
from services.transaction_query_service import search_transactions

router = APIRouter(prefix="/transactions-query", tags=["transactions-query"])


@router.get("/", response_model=list[TransactionQueryResponse])
def list_or_search_transactions(
    user_name: str | None = None,
    username: str | None = None,
    supplier_name: str | None = None,
    product_type_name: str | None = None,
    amount_min: int | None = None,
    amount_max: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Busca transacciones filtrando por:
    - user_name (nombre completo, ej. 'Juan')
    - username (login interno)
    - supplier_name (nombre legal o comercial)
    - product_type_name (ej. 'Lapiz')
    - rango de montos (amount_min / amount_max)
    """
    return search_transactions(
        db,
        user_name=user_name,
        username=username,
        supplier_name=supplier_name,
        product_type_name=product_type_name,
        amount_min=amount_min,
        amount_max=amount_max,
    )

# app/services/product_type_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.product_type import ProductTypes
from app.schemas.product_type_schema import ProductTypeCreate


def create_product_type(db: Session, data: ProductTypeCreate) -> ProductTypes:
    """
    Crea un nuevo tipo de producto.
    Valida que no exista otro con el mismo nombre.
    """
    # Validar duplicado por nombre (case-insensitive)
    existing = (
        db.query(ProductTypes)
        .filter(ProductTypes.name.ilike(data.name))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un tipo de producto con el nombre '{data.name}'.",
        )

    pt = ProductTypes(
        name=data.name,
        description=data.description,
    )
    db.add(pt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error de integridad al crear el tipo de producto '{data.name}'.",
        )

    db.refresh(pt)
    return pt


def search_product_types(
    db: Session,
    pt_id: int | None = None,
    name: str | None = None,
) -> list[ProductTypes]:
    """
    Busca tipos de producto por:
    - id (pt_id)
    - nombre parcial (name)
    Si no se pasa nada, devuelve todos.
    """
    query = db.query(ProductTypes)

    if pt_id is not None:
        query = query.filter(ProductTypes.id == pt_id)

    if name:
        pattern = f"%{name}%"
        query = query.filter(ProductTypes.name.ilike(pattern))

    return query.order_by(ProductTypes.id).all()


def get_product_type(db: Session, pt_id: int) -> ProductTypes | None:
    """
    Obtiene un tipo de producto por ID.
    """
    return db.query(ProductTypes).filter(ProductTypes.id == pt_id).first()


def update_product_type(
    db: Session,
    pt_id: int,
    data: ProductTypeCreate,
) -> ProductTypes | None:
    """
    Actualiza un tipo de producto existente.
    """
    pt = get_product_type(db, pt_id)
    if not pt:
        return None

    # Si cambia el nombre, validar duplicado
    if data.name and data.name != pt.name:
        existing = (
            db.query(ProductTypes)
            .filter(
                ProductTypes.name.ilike(data.name),
                ProductTypes.id != pt_id,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe otro tipo de producto con el nombre '{data.name}'.",
            )

    pt.name = data.name
    pt.description = data.description

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error de integridad al actualizar el tipo de producto.",
        )

    db.refresh(pt)
    return pt


def delete_product_type(db: Session, pt_id: int) -> bool:
    """
    Elimina un tipo de producto por ID.
    Devuelve True si lo eliminó, False si no existía.
    """
    pt = get_product_type(db, pt_id)
    if not pt:
        return False

    db.delete(pt)
    db.commit()
    return True

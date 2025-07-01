from typing import List, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session
from .models import (
    DBProduct,
    Product,
    ProductRead,
    ProductUpdate,
    PaginatedProducts,
)
from base.db_base_services import filter_instances


router: APIRouter = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get(path="/", response_model=PaginatedProducts)
def get_products(
    name: Optional[str] = None,
    product_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """
    Retrieve products (optionally including deleted ones), with optional filtering by fields and pagination.
    Use the product_deleted query parameter to include deleted products if needed.
    """
    filters = {
        "deleted": product_deleted,
        "name": name,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    products, total_count = filter_instances(DBProduct, session, filters, limit=limit, offset=offset)
    results = [ProductRead.model_validate(p) for p in products]
    return PaginatedProducts(results=results, total_count=total_count)


@router.post("/", response_model=ProductRead)
def create_product(
    payload: Product,
    session: Session = Depends(get_session),
) -> DBProduct:
    """Create a new active product."""
    product: Optional[DBProduct] = session.query(DBProduct).filter_by(name=payload.name).first()
    if product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists",
        )
    db_product: DBProduct = DBProduct.create_object(session=session, **payload.model_dump())
    return db_product


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
) -> DBProduct:
    """Get a product by ID."""
    product: Optional[DBProduct] = session.query(DBProduct).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exist.",
        )
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    session: Session = Depends(get_session),
) -> DBProduct:
    """Update an active product."""
    product: Optional[DBProduct] = session.query(DBProduct).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exist.",
        )
    
    # Check if name is being updated and if it conflicts with existing product
    if payload.name and payload.name != product.name:
        existing_product: Optional[DBProduct] = session.query(DBProduct).filter_by(name=payload.name).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists",
            )
    
    product.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a product."""
    product: Optional[DBProduct] = session.query(DBProduct).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exist.",
        )
    product.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from typing import List, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session
from jwt_authentication.decorators import get_current_user
from employees.models import RoleChoices
from employees.utils import require_roles
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
    product_id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    product_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Retrieve products with flexible filtering and pagination.
    
    Filtering options:
    - product_id: Exact match
    - name: Case-insensitive contains search
    - description: Case-insensitive contains search
    - category: Case-insensitive contains search
    - price_min/price_max: Price range filtering
    - created_at_from/created_at_to: Date range filtering
    - updated_at_from/updated_at_to: Date range filtering
    - product_deleted: Boolean filter
    """
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )
    
    # Build query with flexible filtering
    query = session.query(DBProduct)
    
    # Exact match for ID
    if product_id:
        query = query.filter(DBProduct.id == product_id)
    
    # Case-insensitive contains for text fields
    if name:
        query = query.filter(DBProduct.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(DBProduct.description.ilike(f"%{description}%"))
    if category:
        query = query.filter(DBProduct.category.ilike(f"%{category}%"))
    
    # Price range filtering
    if price_min is not None:
        query = query.filter(DBProduct.price >= price_min)
    if price_max is not None:
        query = query.filter(DBProduct.price <= price_max)
    
    # Date range filtering
    if created_at_from:
        query = query.filter(DBProduct.created_at >= created_at_from)
    if created_at_to:
        query = query.filter(DBProduct.created_at <= created_at_to)
    if updated_at_from:
        query = query.filter(DBProduct.updated_at >= updated_at_from)
    if updated_at_to:
        query = query.filter(DBProduct.updated_at <= updated_at_to)
    
    # Boolean filter
    query = query.filter(DBProduct.deleted == product_deleted)
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply pagination
    results = query.offset(offset).limit(limit).all()
    
    # Convert to response models
    results = [ProductRead.model_validate(p) for p in results]
    return PaginatedProducts(results=results, total_count=total_count)


@router.post("/", response_model=ProductRead)
def create_product(
    payload: Product,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProduct:
    """Create a new active product."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
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
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProduct:
    """Get a product by ID."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )
    
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
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProduct:
    """Update an active product."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
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
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a product."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    product: Optional[DBProduct] = session.query(DBProduct).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exist.",
        )
    
    product.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from typing import List, Dict, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session, selectinload
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session
from jwt_authentication.decorators import get_current_user
from employees.models import RoleChoices
from employees.utils import require_roles
from .models import (
    # Sale Order models
    DBSaleOrder,
    SaleOrder,
    SaleOrderRead,
    SaleOrderUpdate,
    PaginatedSaleOrders,
    DBSaleOrderItem,
    SaleOrderItem,
    SaleOrderItemRead,
    SaleOrderItemUpdate,
    # Production Order models
    DBProductionOrder,
    ProductionOrder,
    ProductionOrderRead,
    ProductionOrderUpdate,
    PaginatedProductionOrders,
    DBProductionOrderItem,
    ProductionOrderItem,
    ProductionOrderItemRead,
    ProductionOrderItemUpdate,
    # Quality Evaluation models
    DBQualityEvaluation,
    QualityEvaluation,
    QualityEvaluationRead,
    QualityEvaluationUpdate,
    PaginatedQualityEvaluations,
    DBNonConformingProduct,
    NonConformingProduct,
    NonConformingProductRead,
    NonConformingProductUpdate,
)
from base.db_base_services import filter_instances


router: APIRouter = APIRouter(
    prefix="/production",
    tags=["production"],
)


# Sale Order endpoints
@router.get("/sale-orders/", response_model=PaginatedSaleOrders)
def get_sale_orders(
    client_id: Optional[str] = None,
    sale_order_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedSaleOrders:
    """Retrieve sale orders with optional filtering and pagination."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    filters = {
        "deleted": sale_order_deleted,
        "client_id": client_id,
    }
    filters: Dict = {
        k: v
        for k, v in filters.items()
        if v is not None
    }
    sale_orders, total_count = filter_instances(
        model=DBSaleOrder,
        session=session,
        filters=filters,
        limit=limit,
        offset=offset,
    )
    results: List[SaleOrderRead] = [
        SaleOrderRead.model_validate(so)
        for so in sale_orders
    ]
    return PaginatedSaleOrders(results=results, total_count=total_count)


@router.post("/sale-orders/", response_model=SaleOrderRead)
def create_sale_order(
    payload: SaleOrder,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBSaleOrder:
    """Create a new sale order."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    db_sale_order: DBSaleOrder = DBSaleOrder.create_object(session=session, **payload.model_dump())
    return db_sale_order


@router.get("/sale-orders/{sale_order_id}", response_model=SaleOrderRead)
def get_sale_order(
    sale_order_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBSaleOrder:
    """Get a sale order by ID, including its items."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )
    
    sale_order: Optional[DBSaleOrder] = (
        session.query(DBSaleOrder)
        .options(selectinload(DBSaleOrder.items))
        .filter_by(id=sale_order_id)
        .first()
    )
    if not sale_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order not found",
        )
    return sale_order


@router.put("/sale-orders/{sale_order_id}", response_model=SaleOrderRead)
def update_sale_order(
    sale_order_id: int,
    payload: SaleOrderUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBSaleOrder:
    """Update a sale order."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    sale_order: Optional[DBSaleOrder] = session.query(DBSaleOrder).filter_by(id=sale_order_id).first()
    if not sale_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order not found",
        )
    
    sale_order.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return sale_order


@router.delete("/sale-orders/{sale_order_id}")
def delete_sale_order(
    sale_order_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a sale order."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    sale_order: Optional[DBSaleOrder] = session.query(DBSaleOrder).filter_by(id=sale_order_id).first()
    if not sale_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order not found",
        )
    
    sale_order.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/sale-order-items/", response_model=SaleOrderItemRead)
def create_sale_order_item(
    payload: SaleOrderItem,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBSaleOrderItem:
    """Create a new sale order item."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    db_sale_order_item: DBSaleOrderItem = DBSaleOrderItem.create_object(session=session, **payload.model_dump())
    return db_sale_order_item


@router.put("/sale-order-items/{item_id}", response_model=SaleOrderItemRead)
def update_sale_order_item(
    item_id: int,
    payload: SaleOrderItemUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBSaleOrderItem:
    """Update a sale order item."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    sale_order_item: Optional[DBSaleOrderItem] = session.query(DBSaleOrderItem).filter_by(id=item_id).first()
    if not sale_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order item not found",
        )
    
    sale_order_item.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return sale_order_item


@router.delete("/sale-order-items/{item_id}")
def delete_sale_order_item(
    item_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a sale order item."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    sale_order_item: Optional[DBSaleOrderItem] = session.query(DBSaleOrderItem).filter_by(id=item_id).first()
    if not sale_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order item not found",
        )
    
    sale_order_item.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Production Order endpoints
@router.get("/production-orders/", response_model=PaginatedProductionOrders)
def get_production_orders(
    production_order_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Retrieve production orders with optional filtering and pagination."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )
    
    filters = {
        "deleted": production_order_deleted,
    }
    production_orders, total_count = filter_instances(
        model=DBProductionOrder,
        session=session,
        filters=filters,
        limit=limit,
        offset=offset,
    )
    results: List[ProductionOrderRead] = [
        ProductionOrderRead.model_validate(po)
        for po in production_orders
    ]
    return PaginatedProductionOrders(results=results, total_count=total_count)


@router.post("/production-orders/", response_model=ProductionOrderRead)
def create_production_order(
    payload: ProductionOrder,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProductionOrder:
    """Create a new production order."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    db_production_order: DBProductionOrder = DBProductionOrder.create_object(session=session, **payload.model_dump())
    return db_production_order


@router.get("/production-orders/{production_order_id}", response_model=ProductionOrderRead)
def get_production_order(
    production_order_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProductionOrder:
    """Get a production order by ID, including its items."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )
    
    production_order: Optional[DBProductionOrder] = (
        session.query(DBProductionOrder)
        .options(selectinload(DBProductionOrder.items))
        .filter_by(id=production_order_id)
        .first()
    )
    if not production_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order not found",
        )
    return production_order


@router.put("/production-orders/{production_order_id}", response_model=ProductionOrderRead)
def update_production_order(
    production_order_id: int,
    payload: ProductionOrderUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProductionOrder:
    """Update a production order."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    production_order: Optional[DBProductionOrder] = session.query(DBProductionOrder).filter_by(id=production_order_id).first()
    if not production_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order not found",
        )
    
    production_order.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return production_order


@router.delete("/production-orders/{production_order_id}")
def delete_production_order(
    production_order_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a production order."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    production_order: Optional[DBProductionOrder] = session.query(DBProductionOrder).filter_by(id=production_order_id).first()
    if not production_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order not found",
        )
    
    production_order.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/production-order-items/", response_model=ProductionOrderItemRead)
def create_production_order_item(
    payload: ProductionOrderItem,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProductionOrderItem:
    """Create a new production order item."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    db_production_order_item: DBProductionOrderItem = DBProductionOrderItem.create_object(session=session, **payload.model_dump())
    return db_production_order_item


@router.put("/production-order-items/{item_id}", response_model=ProductionOrderItemRead)
def update_production_order_item(
    item_id: int,
    payload: ProductionOrderItemUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBProductionOrderItem:
    """Update a production order item."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    production_order_item: Optional[DBProductionOrderItem] = session.query(DBProductionOrderItem).filter_by(id=item_id).first()
    if not production_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order item not found",
        )
    
    production_order_item.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return production_order_item


@router.delete("/production-order-items/{item_id}")
def delete_production_order_item(
    item_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a production order item."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    production_order_item: Optional[DBProductionOrderItem] = session.query(DBProductionOrderItem).filter_by(id=item_id).first()
    if not production_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order item not found",
        )
    
    production_order_item.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Quality Evaluation endpoints
@router.get("/quality-evaluations/", response_model=PaginatedQualityEvaluations)
def get_quality_evaluations(
    sale_order_id: Optional[int] = None,
    quality_evaluation_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Retrieve quality evaluations with optional filtering and pagination."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    filters = {
        "deleted": quality_evaluation_deleted,
        "sale_order_id": sale_order_id,
    }
    filters: Dict = {
        k: v
        for k, v in filters.items()
        if v is not None
    }
    quality_evaluations, total_count = filter_instances(
        model=DBQualityEvaluation,
        session=session,
        filters=filters,
        limit=limit,
        offset=offset,
    )
    results: List[QualityEvaluationRead] = [
        QualityEvaluationRead.model_validate(qe)
        for qe in quality_evaluations
    ]
    return PaginatedQualityEvaluations(results=results, total_count=total_count)


@router.post("/quality-evaluations/", response_model=QualityEvaluationRead)
def create_quality_evaluation(
    payload: QualityEvaluation,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBQualityEvaluation:
    """Create a new quality evaluation."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    db_quality_evaluation: DBQualityEvaluation = DBQualityEvaluation.create_object(session=session, **payload.model_dump())
    return db_quality_evaluation


@router.get("/quality-evaluations/{evaluation_id}", response_model=QualityEvaluationRead)
def get_quality_evaluation(
    evaluation_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBQualityEvaluation:
    """Get a quality evaluation by ID, including its non-conforming products."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    quality_evaluation: Optional[DBQualityEvaluation] = (
        session.query(DBQualityEvaluation)
        .options(selectinload(DBQualityEvaluation.non_conforming_products))
        .filter_by(id=evaluation_id)
        .first()
    )
    if not quality_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation not found",
        )
    return quality_evaluation


@router.put("/quality-evaluations/{evaluation_id}", response_model=QualityEvaluationRead)
def update_quality_evaluation(
    evaluation_id: int,
    payload: QualityEvaluationUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBQualityEvaluation:
    """Update a quality evaluation."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    quality_evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not quality_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation not found",
        )
    
    quality_evaluation.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return quality_evaluation


@router.delete("/quality-evaluations/{evaluation_id}")
def delete_quality_evaluation(
    evaluation_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a quality evaluation."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    quality_evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not quality_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation not found",
        )
    
    quality_evaluation.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/quality-evaluations/{evaluation_id}/available-non-conforming-products", response_model=List[SaleOrderItemRead])
def get_available_non_conforming_products(
    evaluation_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get available non-conforming products for a quality evaluation."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    quality_evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not quality_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation not found",
        )
    
    available_products = quality_evaluation.non_conforming_product_types(session)
    return available_products


@router.post("/non-conforming-products/", response_model=NonConformingProductRead)
def create_non_conforming_product(
    payload: NonConformingProduct,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBNonConformingProduct:
    """Create a new non-conforming product."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    # Validate that the quality evaluation exists
    quality_evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(
        id=payload.quality_evaluation_id
    ).first()
    if not quality_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation not found",
        )
    
    # Validate that the sale order item exists and belongs to the quality evaluation's sale order
    sale_order_item: Optional[DBSaleOrderItem] = session.query(DBSaleOrderItem).filter_by(
        id=payload.non_conforming_product_id
    ).first()
    if not sale_order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order item not found",
        )
    
    if sale_order_item.sale_order_id != quality_evaluation.sale_order_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sale order item does not belong to the quality evaluation's sale order",
        )
    
    # Validate that the item can be marked as non-conforming
    if not quality_evaluation.can_mark_as_non_conforming(session, payload.non_conforming_product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item cannot be marked as non-conforming",
        )
    
    db_non_conforming_product: DBNonConformingProduct = DBNonConformingProduct.create_object(
        session=session, **payload.model_dump()
    )
    return db_non_conforming_product


@router.put("/non-conforming-products/{product_id}", response_model=NonConformingProductRead)
def update_non_conforming_product(
    product_id: int,
    payload: NonConformingProductUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBNonConformingProduct:
    """Update a non-conforming product."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    non_conforming_product: Optional[DBNonConformingProduct] = session.query(DBNonConformingProduct).filter_by(id=product_id).first()
    if not non_conforming_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-conforming product not found",
        )
    
    non_conforming_product.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return non_conforming_product


@router.delete("/non-conforming-products/{product_id}")
def delete_non_conforming_product(
    product_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a non-conforming product."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.QUALITY,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )
    
    non_conforming_product: Optional[DBNonConformingProduct] = session.query(DBNonConformingProduct).filter_by(id=product_id).first()
    if not non_conforming_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-conforming product not found",
        )
    
    non_conforming_product.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

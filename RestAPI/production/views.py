from typing import List, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session, selectinload
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session
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
    session: Session = Depends(get_session),
):
    """Retrieve sale orders with optional filtering and pagination."""
    filters = {
        "deleted": sale_order_deleted,
        "client_id": client_id,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    sale_orders, total_count = filter_instances(DBSaleOrder, session, filters, limit=limit, offset=offset)
    results = [SaleOrderRead.model_validate(so) for so in sale_orders]
    return PaginatedSaleOrders(results=results, total_count=total_count)


@router.post("/sale-orders/", response_model=SaleOrderRead)
def create_sale_order(
    payload: SaleOrder,
    session: Session = Depends(get_session),
) -> DBSaleOrder:
    """Create a new sale order."""
    db_sale_order: DBSaleOrder = DBSaleOrder.create_object(session=session, **payload.model_dump())
    return db_sale_order


@router.get("/sale-orders/{sale_order_id}", response_model=SaleOrderRead)
def get_sale_order(
    sale_order_id: int,
    session: Session = Depends(get_session),
) -> DBSaleOrder:
    """Get a sale order by ID, including its items."""
    sale_order: Optional[DBSaleOrder] = (
        session.query(DBSaleOrder)
        .options(selectinload(DBSaleOrder.items))
        .filter_by(id=sale_order_id)
        .first()
    )
    if not sale_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order doesn't exist.",
        )
    return sale_order


@router.put("/sale-orders/{sale_order_id}", response_model=SaleOrderRead)
def update_sale_order(
    sale_order_id: int,
    payload: SaleOrderUpdate,
    session: Session = Depends(get_session),
) -> DBSaleOrder:
    """Update a sale order."""
    sale_order: Optional[DBSaleOrder] = session.query(DBSaleOrder).filter_by(id=sale_order_id).first()
    if not sale_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order doesn't exist.",
        )
    sale_order.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return sale_order


@router.delete("/sale-orders/{sale_order_id}")
def delete_sale_order(
    sale_order_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a sale order."""
    sale_order: Optional[DBSaleOrder] = session.query(DBSaleOrder).filter_by(id=sale_order_id).first()
    if not sale_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order doesn't exist.",
        )
    sale_order.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Sale Order Item endpoints
@router.post("/sale-order-items/", response_model=SaleOrderItemRead)
def create_sale_order_item(
    payload: SaleOrderItem,
    session: Session = Depends(get_session),
) -> DBSaleOrderItem:
    """Create a new sale order item."""
    db_item: DBSaleOrderItem = DBSaleOrderItem.create_object(session=session, **payload.model_dump())
    return db_item


@router.put("/sale-order-items/{item_id}", response_model=SaleOrderItemRead)
def update_sale_order_item(
    item_id: int,
    payload: SaleOrderItemUpdate,
    session: Session = Depends(get_session),
) -> DBSaleOrderItem:
    """Update a sale order item."""
    item: Optional[DBSaleOrderItem] = session.query(DBSaleOrderItem).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order item doesn't exist.",
        )
    item.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return item


@router.delete("/sale-order-items/{item_id}")
def delete_sale_order_item(
    item_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a sale order item."""
    item: Optional[DBSaleOrderItem] = session.query(DBSaleOrderItem).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale order item doesn't exist.",
        )
    item.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Production Order endpoints
@router.get("/production-orders/", response_model=PaginatedProductionOrders)
def get_production_orders(
    production_order_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Retrieve production orders with optional filtering and pagination."""
    filters = {
        "deleted": production_order_deleted,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    production_orders, total_count = filter_instances(DBProductionOrder, session, filters, limit=limit, offset=offset)
    results = [ProductionOrderRead.model_validate(po) for po in production_orders]
    return PaginatedProductionOrders(results=results, total_count=total_count)


@router.post("/production-orders/", response_model=ProductionOrderRead)
def create_production_order(
    payload: ProductionOrder,
    session: Session = Depends(get_session),
) -> DBProductionOrder:
    """Create a new production order."""
    db_production_order: DBProductionOrder = DBProductionOrder.create_object(session=session, **payload.model_dump())
    return db_production_order


@router.get("/production-orders/{production_order_id}", response_model=ProductionOrderRead)
def get_production_order(
    production_order_id: int,
    session: Session = Depends(get_session),
) -> DBProductionOrder:
    """Get a production order by ID, including its items."""
    production_order: Optional[DBProductionOrder] = (
        session.query(DBProductionOrder)
        .options(selectinload(DBProductionOrder.items))
        .filter_by(id=production_order_id)
        .first()
    )
    if not production_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order doesn't exist.",
        )
    return production_order


@router.put("/production-orders/{production_order_id}", response_model=ProductionOrderRead)
def update_production_order(
    production_order_id: int,
    payload: ProductionOrderUpdate,
    session: Session = Depends(get_session),
) -> DBProductionOrder:
    """Update a production order."""
    production_order: Optional[DBProductionOrder] = session.query(DBProductionOrder).filter_by(id=production_order_id).first()
    if not production_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order doesn't exist.",
        )
    production_order.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return production_order


@router.delete("/production-orders/{production_order_id}")
def delete_production_order(
    production_order_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a production order."""
    production_order: Optional[DBProductionOrder] = session.query(DBProductionOrder).filter_by(id=production_order_id).first()
    if not production_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order doesn't exist.",
        )
    production_order.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/production-order-items/", response_model=ProductionOrderItemRead)
def create_production_order_item(
    payload: ProductionOrderItem,
    session: Session = Depends(get_session),
) -> DBProductionOrderItem:
    """Create a new production order item."""
    db_item: DBProductionOrderItem = DBProductionOrderItem.create_object(session=session, **payload.model_dump())
    return db_item


@router.put("/production-order-items/{item_id}", response_model=ProductionOrderItemRead)
def update_production_order_item(
    item_id: int,
    payload: ProductionOrderItemUpdate,
    session: Session = Depends(get_session),
) -> DBProductionOrderItem:
    """Update a production order item."""
    item: Optional[DBProductionOrderItem] = session.query(DBProductionOrderItem).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order item doesn't exist.",
        )
    item.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return item


@router.delete("/production-order-items/{item_id}")
def delete_production_order_item(
    item_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a production order item."""
    item: Optional[DBProductionOrderItem] = session.query(DBProductionOrderItem).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order item doesn't exist.",
        )
    item.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Quality Evaluation endpoints
@router.get("/quality-evaluations/", response_model=PaginatedQualityEvaluations)
def get_quality_evaluations(
    sale_order_id: Optional[int] = None,
    quality_evaluation_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Retrieve quality evaluations with optional filtering and pagination."""
    filters = {
        "deleted": quality_evaluation_deleted,
        "sale_order_id": sale_order_id,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    evaluations, total_count = filter_instances(DBQualityEvaluation, session, filters, limit=limit, offset=offset)
    results = [QualityEvaluationRead.model_validate(eval) for eval in evaluations]
    return PaginatedQualityEvaluations(results=results, total_count=total_count)


@router.post("/quality-evaluations/", response_model=QualityEvaluationRead)
def create_quality_evaluation(
    payload: QualityEvaluation,
    session: Session = Depends(get_session),
) -> DBQualityEvaluation:
    """Create a new quality evaluation."""
    db_evaluation: DBQualityEvaluation = DBQualityEvaluation.create_object(session=session, **payload.model_dump())
    return db_evaluation


@router.get("/quality-evaluations/{evaluation_id}", response_model=QualityEvaluationRead)
def get_quality_evaluation(
    evaluation_id: int,
    session: Session = Depends(get_session),
) -> DBQualityEvaluation:
    """Get a quality evaluation by ID."""
    evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation doesn't exist.",
        )
    return evaluation


@router.put("/quality-evaluations/{evaluation_id}", response_model=QualityEvaluationRead)
def update_quality_evaluation(
    evaluation_id: int,
    payload: QualityEvaluationUpdate,
    session: Session = Depends(get_session),
) -> DBQualityEvaluation:
    """Update a quality evaluation."""
    evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation doesn't exist.",
        )
    evaluation.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return evaluation


@router.delete("/quality-evaluations/{evaluation_id}")
def delete_quality_evaluation(
    evaluation_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a quality evaluation."""
    evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation doesn't exist.",
        )
    evaluation.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/quality-evaluations/{evaluation_id}/available-non-conforming-products", response_model=List[SaleOrderItemRead])
def get_available_non_conforming_products(
    evaluation_id: int,
    session: Session = Depends(get_session),
):
    """
    Get all sale order items that can be selected as non-conforming products for a specific quality evaluation.
    These are the items from the associated sale order that are available to be marked as non-conforming.
    """
    evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(id=evaluation_id).first()
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation doesn't exist.",
        )

    available_products = evaluation.non_conforming_product_types(session)
    return available_products


# Non-Conforming Product endpoints
@router.post("/non-conforming-products/", response_model=NonConformingProductRead)
def create_non_conforming_product(
    payload: NonConformingProduct,
    session: Session = Depends(get_session),
) -> DBNonConformingProduct:
    """Create a new non-conforming product record."""
    # Validate that the quality evaluation exists
    quality_evaluation: Optional[DBQualityEvaluation] = session.query(DBQualityEvaluation).filter_by(
        id=payload.quality_evaluation_id
    ).first()
    if not quality_evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality evaluation doesn't exist.",
        )

    # Validate that the sale order item can be marked as non-conforming
    if not quality_evaluation.can_mark_as_non_conforming(session, payload.non_conforming_product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This sale order item cannot be marked as non-conforming. It may not exist in the sale order or may already be marked as non-conforming.",
        )

    db_product: DBNonConformingProduct = DBNonConformingProduct.create_object(session=session, **payload.model_dump())
    return db_product


@router.put("/non-conforming-products/{product_id}", response_model=NonConformingProductRead)
def update_non_conforming_product(
    product_id: int,
    payload: NonConformingProductUpdate,
    session: Session = Depends(get_session),
) -> DBNonConformingProduct:
    """Update a non-conforming product."""
    product: Optional[DBNonConformingProduct] = session.query(DBNonConformingProduct).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-conforming product doesn't exist.",
        )
    product.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return product


@router.delete("/non-conforming-products/{product_id}")
def delete_non_conforming_product(
    product_id: int,
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a non-conforming product."""
    product: Optional[DBNonConformingProduct] = session.query(DBNonConformingProduct).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Non-conforming product doesn't exist.",
        )
    product.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

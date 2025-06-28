from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.production.models import SaleOrder, ProductionOrder, QualityEvaluation
from app.production.schemas import (
    SaleOrderCreate,
    SaleOrder,
    ProductionOrderCreate,
    ProductionOrder,
    QualityEvaluationCreate,
    QualityEvaluation
)
from app.production.services import (
    create_sale_order,
    get_sale_orders,
    create_production_order,
    create_quality_evaluation
)
from typing import List

router = APIRouter()

@router.post("/sale-orders/", response_model=SaleOrder, tags=["production"])
async def create_sale_order_endpoint(order_in: SaleOrderCreate, db: Session = Depends(get_db)):
    """
    Create a new sale order with its items.
    - **order_in**: Sale order data including items
    - Returns: Created sale order object
    """
    return create_sale_order(db, order_in)

@router.get("/sale-orders/", response_model=List[SaleOrder], tags=["production"])
async def get_sale_orders_endpoint(db: Session = Depends(get_db)):
    """
    Get all sale orders.
    - Returns: List of all sale orders
    """
    return get_sale_orders(db)

@router.post("/production-orders/", response_model=ProductionOrder, tags=["production"])
async def create_production_order_endpoint(order_in: ProductionOrderCreate, db: Session = Depends(get_db)):
    """
    Create a new production order with its items.
    - **order_in**: Production order data including items
    - Returns: Created production order object
    """
    return create_production_order(db, order_in)

@router.post("/quality-evaluations/", response_model=QualityEvaluation, tags=["production"])
async def create_quality_evaluation_endpoint(evaluation_in: QualityEvaluationCreate, db: Session = Depends(get_db)):
    """
    Create a new quality evaluation with its non-conforming products.
    - **evaluation_in**: Quality evaluation data including non-conforming products
    - Returns: Created quality evaluation object
    """
    return create_quality_evaluation(db, evaluation_in)

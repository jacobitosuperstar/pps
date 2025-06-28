from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.production import SaleOrder, SaleOrderItem, ProductionOrder, ProductionOrderItem, QualityEvaluation, NonConformingProduct
from app.schemas.production import SaleOrderCreate, SaleOrder, ProductionOrderCreate, ProductionOrder, QualityEvaluationCreate, QualityEvaluation

router = APIRouter()

@router.post("/sale-orders/", response_model=SaleOrder, tags=["production"])
async def create_sale_order(order_in: SaleOrderCreate, db: Session = Depends(get_db)):
    """
    Create a new sale order with its items.
    - **order_in**: Sale order data including items
    - Returns: Created sale order object
    """
    db_order = SaleOrder(
        client_id=order_in.client_id,
        notes=order_in.notes
    )
    db.add(db_order)
    db.flush()
    
    for item in order_in.items:
        db_item = SaleOrderItem(
            order_id=db_order.id,
            product_id=item["product_id"],
            product_amount=item["product_amount"]
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/sale-orders/", response_model=List[SaleOrder], tags=["production"])
async def get_sale_orders(db: Session = Depends(get_db)):
    """
    Get all sale orders.
    - Returns: List of all sale orders
    """
    return db.query(SaleOrder).all()

@router.post("/production-orders/", response_model=ProductionOrder, tags=["production"])
async def create_production_order(order_in: ProductionOrderCreate, db: Session = Depends(get_db)):
    """
    Create a new production order with its items.
    - **order_in**: Production order data including items
    - Returns: Created production order object
    """
    db_order = ProductionOrder(
        client_id=order_in.client_id,
        notes=order_in.notes
    )
    db.add(db_order)
    db.flush()
    
    for item in order_in.items:
        db_item = ProductionOrderItem(
            order_id=db_order.id,
            product_id=item["product_id"],
            product_amount=item["product_amount"]
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.post("/quality-evaluations/", response_model=QualityEvaluation, tags=["production"])
async def create_quality_evaluation(evaluation_in: QualityEvaluationCreate, db: Session = Depends(get_db)):
    """
    Create a new quality evaluation with its non-conforming products.
    - **evaluation_in**: Quality evaluation data including non-conforming products
    - Returns: Created quality evaluation object
    """
    db_evaluation = QualityEvaluation(
        sale_order_id=evaluation_in.sale_order_id,
        notes=evaluation_in.notes,
        delivery_date=evaluation_in.delivery_date
    )
    db.add(db_evaluation)
    db.flush()
    
    for product in evaluation_in.non_conforming_products:
        db_product = NonConformingProduct(
            evaluation_id=db_evaluation.id,
            product_id=product["product_id"],
            amount=product["amount"]
        )
        db.add(db_product)
    
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

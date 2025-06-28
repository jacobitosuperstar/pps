from sqlalchemy.orm import Session
from typing import List
from app.production.models import (
    SaleOrder,
    SaleOrderItem,
    ProductionOrder,
    ProductionOrderItem,
    QualityEvaluation,
    NonConformingProduct
)
from app.production.schemas import (
    SaleOrderCreate,
    ProductionOrderCreate,
    QualityEvaluationCreate
)

def create_sale_order(db: Session, order_in: SaleOrderCreate) -> SaleOrder:
    """Create a new sale order with its items."""
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

def get_sale_orders(db: Session) -> List[SaleOrder]:
    """Get all sale orders."""
    return db.query(SaleOrder).all()

def create_production_order(db: Session, order_in: ProductionOrderCreate) -> ProductionOrder:
    """Create a new production order with its items."""
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

def create_quality_evaluation(db: Session, evaluation_in: QualityEvaluationCreate) -> QualityEvaluation:
    """Create a new quality evaluation with its non-conforming products."""
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

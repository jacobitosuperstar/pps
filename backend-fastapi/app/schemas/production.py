from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class SaleOrderBase(BaseModel):
    client_id: str
    notes: Optional[str] = None

class SaleOrderCreate(SaleOrderBase):
    items: List[dict]  # Lista de {product_id: int, product_amount: int}

class SaleOrder(SaleOrderBase):
    id: int
    created_at: date
    items: List[dict]

    class Config:
        from_attributes = True

class ProductionOrderBase(BaseModel):
    client_id: str
    notes: Optional[str] = None

class ProductionOrderCreate(ProductionOrderBase):
    items: List[dict]  # Lista de {product_id: int, product_amount: int}

class ProductionOrder(ProductionOrderBase):
    id: int
    created_at: date
    items: List[dict]

    class Config:
        from_attributes = True

class QualityEvaluationBase(BaseModel):
    sale_order_id: int
    notes: Optional[str] = None
    delivery_date: date

class QualityEvaluationCreate(QualityEvaluationBase):
    non_conforming_products: List[dict]  # Lista de {product_id: int, amount: int}

class QualityEvaluation(QualityEvaluationBase):
    id: int
    non_conforming_products: List[dict]

    class Config:
        from_attributes = True

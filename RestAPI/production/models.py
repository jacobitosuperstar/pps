from typing import Optional, List
from datetime import datetime, date

from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict

from base.models import Base, PaginatedElements
from clients.models import DBClient
from products.models import DBProduct


class DBSaleOrder(Base):
    """Sale order for production."""
    __tablename__ = "sale_order"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    client_id = Column(
        String,
        ForeignKey("client.client_id"),
        nullable=False,
    )
    notes = Column(
        Text,
        nullable=True,
    )

    # Relationships
    client = relationship("DBClient", back_populates="sale_orders")
    items = relationship("DBSaleOrderItem", back_populates="sale_order", cascade="all, delete-orphan")


class SaleOrder(BaseModel):
    client_id: str = Field(..., description="Client ID for the sale order")
    notes: Optional[str] = Field(None, description="Notes from the commercial")


class SaleOrderUpdate(BaseModel):
    client_id: Optional[str] = Field(None, description="Client ID for the sale order")
    notes: Optional[str] = Field(None, description="Notes from the commercial")


class SaleOrderRead(SaleOrder):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool
    items: List["SaleOrderItemRead"] = []

    model_config = ConfigDict(from_attributes=True)


class DBSaleOrderItem(Base):
    """Items in a sale order."""
    __tablename__ = "sale_order_item"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    sale_order_id = Column(
        Integer,
        ForeignKey("sale_order.id"),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey("product.id"),
        nullable=False,
    )
    product_amount = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # Relationships
    sale_order = relationship("DBSaleOrder", back_populates="items")
    product = relationship("DBProduct", back_populates="sale_order_items")


class SaleOrderItem(BaseModel):
    sale_order_id: int = Field(..., description="Sale order ID")
    product_id: int = Field(..., description="Product ID")
    product_amount: int = Field(0, ge=0, description="Amount of product needed")


class SaleOrderItemUpdate(BaseModel):
    sale_order_id: Optional[int] = Field(None, description="Sale order ID")
    product_id: Optional[int] = Field(None, description="Product ID")
    product_amount: Optional[int] = Field(None, ge=0, description="Amount of product needed")


class SaleOrderItemRead(SaleOrderItem):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


class DBProductionOrder(Base):
    """Production order."""
    __tablename__ = "production_order"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    notes = Column(
        Text,
        nullable=True,
    )

    # Relationships
    items = relationship("DBProductionOrderItem", back_populates="production_order", cascade="all, delete-orphan")


class ProductionOrder(BaseModel):
    notes: Optional[str] = Field(None, description="Notes from the commercial")


class ProductionOrderUpdate(BaseModel):
    notes: Optional[str] = Field(None, description="Notes from the commercial")


class ProductionOrderRead(ProductionOrder):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool
    items: List["ProductionOrderItemRead"] = []

    model_config = ConfigDict(from_attributes=True)


class DBProductionOrderItem(Base):
    """Items in a production order."""
    __tablename__ = "production_order_item"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    production_order_id = Column(
        Integer,
        ForeignKey("production_order.id"),
        nullable=False,
    )
    product_id = Column(
        Integer,
        ForeignKey("product.id"),
        nullable=False,
    )
    product_amount = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # Relationships
    production_order = relationship("DBProductionOrder", back_populates="items")
    product = relationship("DBProduct", back_populates="production_order_items")


class ProductionOrderItem(BaseModel):
    production_order_id: int = Field(..., description="Production order ID")
    product_id: int = Field(..., description="Product ID")
    product_amount: int = Field(0, ge=0, description="Amount of product needed")


class ProductionOrderItemUpdate(BaseModel):
    production_order_id: Optional[int] = Field(None, description="Production order ID")
    product_id: Optional[int] = Field(None, description="Product ID")
    product_amount: Optional[int] = Field(None, ge=0, description="Amount of product needed")


class ProductionOrderItemRead(ProductionOrderItem):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


class DBQualityEvaluation(Base):
    """Quality evaluation of production orders."""
    __tablename__ = "quality_evaluation"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    sale_order_id = Column(
        Integer,
        ForeignKey("sale_order.id"),
        nullable=False,
    )
    notes = Column(
        Text,
        nullable=True,
    )
    delivery_date = Column(
        Date,
        nullable=False,
    )

    # Relationships
    sale_order = relationship("DBSaleOrder")
    non_conforming_products = relationship("DBNonConformingProduct", back_populates="quality_evaluation", cascade="all, delete-orphan")

    def non_conforming_product_types(self, session) -> List[SaleOrderItemRead]:
        """
        Returns all the sale order items that can be selected as non-conforming products.
        These are the items from the associated sale order that haven't been marked as non-conforming yet.
        """
        from .models import DBSaleOrderItem, SaleOrderItemRead
        
        # Get all sale order items for this quality evaluation's sale order
        sale_order_items = session.query(DBSaleOrderItem).filter(
            DBSaleOrderItem.sale_order_id == self.sale_order_id,
            DBSaleOrderItem.deleted == False
        ).all()
        
        # Return Pydantic objects directly
        return [SaleOrderItemRead.model_validate(item) for item in sale_order_items]

    def can_mark_as_non_conforming(self, session, sale_order_item_id: int) -> bool:
        """
        Validates if a sale order item can be marked as non-conforming.
        Returns True if the item exists in the associated sale order and hasn't been marked as non-conforming yet.
        """
        from .models import DBSaleOrderItem, DBNonConformingProduct
        
        # Check if the sale order item exists and belongs to this quality evaluation's sale order
        sale_order_item = session.query(DBSaleOrderItem).filter(
            DBSaleOrderItem.id == sale_order_item_id,
            DBSaleOrderItem.sale_order_id == self.sale_order_id,
            DBSaleOrderItem.deleted == False
        ).first()
        
        if not sale_order_item:
            return False
        
        # Check if this item is already marked as non-conforming in this quality evaluation
        existing_non_conforming = session.query(DBNonConformingProduct).filter(
            DBNonConformingProduct.quality_evaluation_id == self.id,
            DBNonConformingProduct.non_conforming_product_id == sale_order_item_id,
            DBNonConformingProduct.deleted == False
        ).first()
        
        return existing_non_conforming is None


class QualityEvaluation(BaseModel):
    sale_order_id: int = Field(..., description="Sale order ID")
    notes: Optional[str] = Field(None, description="Observations from quality personnel")
    delivery_date: date = Field(..., description="Date when the order was delivered")


class QualityEvaluationUpdate(BaseModel):
    sale_order_id: Optional[int] = Field(None, description="Sale order ID")
    notes: Optional[str] = Field(None, description="Observations from quality personnel")
    delivery_date: Optional[date] = Field(None, description="Date when the order was delivered")


class QualityEvaluationRead(QualityEvaluation):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool
    non_conforming_products: List["NonConformingProductRead"] = []

    model_config = ConfigDict(from_attributes=True)


class DBNonConformingProduct(Base):
    """Non-conforming products in quality evaluations."""
    __tablename__ = "non_conforming_product"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    quality_evaluation_id = Column(
        Integer,
        ForeignKey("quality_evaluation.id"),
        nullable=False,
    )
    non_conforming_product_id = Column(
        Integer,
        ForeignKey("sale_order_item.id"),
        nullable=False,
    )
    non_conforming_product_amount = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # Relationships
    quality_evaluation = relationship("DBQualityEvaluation", back_populates="non_conforming_products")
    non_conforming_product = relationship("DBSaleOrderItem")


class NonConformingProduct(BaseModel):
    quality_evaluation_id: int = Field(..., description="Quality evaluation ID")
    non_conforming_product_id: int = Field(..., description="Sale order item ID")
    non_conforming_product_amount: int = Field(0, ge=0, description="Amount of non-conforming product")


class NonConformingProductUpdate(BaseModel):
    quality_evaluation_id: Optional[int] = Field(None, description="Quality evaluation ID")
    non_conforming_product_id: Optional[int] = Field(None, description="Sale order item ID")
    non_conforming_product_amount: Optional[int] = Field(None, ge=0, description="Amount of non-conforming product")


class NonConformingProductRead(NonConformingProduct):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


PaginatedSaleOrders = PaginatedElements[SaleOrderRead]
PaginatedProductionOrders = PaginatedElements[ProductionOrderRead]
PaginatedQualityEvaluations = PaginatedElements[QualityEvaluationRead]
PaginatedNonConformingProducts = PaginatedElements[NonConformingProductRead]
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class SaleOrder(Base):
    __tablename__ = "sale_orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"))
    notes = Column(Text, nullable=True)

    client = relationship("Client", backref="sale_orders")
    items = relationship("SaleOrderItem", backref="order")
    quality_evaluations = relationship("QualityEvaluation", backref="sale_order")

class SaleOrderItem(Base):
    __tablename__ = "sale_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sale_orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_amount = Column(Integer, default=0)

    product = relationship("Product", backref="sale_order_items")

class ProductionOrder(Base):
    __tablename__ = "production_orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"))
    notes = Column(Text, nullable=True)

    client = relationship("Client", backref="production_orders")
    items = relationship("ProductionOrderItem", backref="order")

class ProductionOrderItem(Base):
    __tablename__ = "production_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("production_orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_amount = Column(Integer, default=0)

    product = relationship("Product", backref="production_order_items")

class QualityEvaluation(Base):
    __tablename__ = "quality_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    sale_order_id = Column(Integer, ForeignKey("sale_orders.id"))
    notes = Column(Text, nullable=True)
    delivery_date = Column(Date, nullable=False)

    non_conforming_products = relationship("NonConformingProduct", backref="evaluation")

class NonConformingProduct(Base):
    __tablename__ = "non_conforming_products"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("quality_evaluations.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    amount = Column(Integer, default=0)

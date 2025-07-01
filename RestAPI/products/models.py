from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict, field_validator

from base.models import Base, PaginatedElements


class DBProduct(Base):
    """
    Items created from the company that are being sold to different clients.

    Attributes:
        id: Unique identifier for the product.
        name: Name of the product.
        materials: Dictionary of materials and amounts needed for the creation of the product.
        created_at: When the record was created.
        updated_at: When the record was last updated.
        deleted: Soft delete flag.
    """
    __tablename__ = "product"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
        unique=True,
    )
    materials = Column(
        JSON,
        nullable=True,
    )

    # Relationships
    sale_order_items = relationship("DBSaleOrderItem", back_populates="product")
    production_order_items = relationship("DBProductionOrderItem", back_populates="product")


class Product(BaseModel):
    name: str = Field(
        ...,
        max_length=255,
        description="Name of the product",
    )
    materials: Optional[Dict[str, Any]] = Field(
        None,
        description="Dictionary of materials and amounts needed for the creation of the product",
    )

    @field_validator('name')
    @classmethod
    def name_to_lowercase(cls, v: str) -> str:
        """Convert product name to lowercase."""
        return v.lower() if v else v

    @field_validator('materials')
    @classmethod
    def materials_keys_to_lowercase(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Convert all keys in materials dictionary to lowercase."""
        if v is not None:
            return {k.lower(): v for k, v in v.items()}
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=255,
        description="Name of the product",
    )
    materials: Optional[Dict[str, Any]] = Field(
        None,
        description="Dictionary of materials and amounts needed for the creation of the product",
    )

    @field_validator('name')
    @classmethod
    def name_to_lowercase(cls, v: Optional[str]) -> Optional[str]:
        """Convert product name to lowercase if provided."""
        return v.lower() if v else v

    @field_validator('materials')
    @classmethod
    def materials_keys_to_lowercase(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Convert all keys in materials dictionary to lowercase if provided."""
        if v is not None:
            return {k.lower(): v for k, v in v.items()}
        return v


class ProductRead(Product):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


# Type alias for paginated products
PaginatedProducts = PaginatedElements[ProductRead]

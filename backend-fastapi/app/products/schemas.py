from pydantic import BaseModel, Field
from typing import Optional, Dict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    materials: Optional[Dict] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

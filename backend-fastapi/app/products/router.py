from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.products.models import Product
from app.products.schemas import ProductCreate, Product
from app.products.services import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product
)

router = APIRouter()

@router.post("/products/", response_model=Product, tags=["products"])
async def create_product_endpoint(product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    - **product_in**: Product data to create
    - Returns: Created product object
    """
    return create_product(db, product_in)

@router.get("/products/", response_model=List[Product], tags=["products"])
async def get_products_endpoint(db: Session = Depends(get_db)):
    """
    Get all products.
    - Returns: List of all products
    """
    return get_products(db)

@router.get("/products/{product_id}", response_model=Product, tags=["products"])
async def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    """
    Get product by ID.
    - **product_id**: Product ID
    - Returns: Product object
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=Product, tags=["products"])
async def update_product_endpoint(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Update product data.
    - **product_id**: Product ID
    - **product_in**: Updated product data
    - Returns: Updated product object
    """
    product = update_product(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}", tags=["products"])
async def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    """
    Delete product by ID.
    - **product_id**: Product ID
    """
    delete_product(db, product_id)
    return {"message": "Product deleted successfully"}

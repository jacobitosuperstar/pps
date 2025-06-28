from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.products import Product
from app.schemas.products import ProductCreate, Product

router = APIRouter()

@router.post("/products/", response_model=Product, tags=["products"])
async def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    - **product_in**: Product data to create
    - Returns: Created product object
    """
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=List[Product], tags=["products"])
async def get_products(db: Session = Depends(get_db)):
    """
    Get all products.
    - Returns: List of all products
    """
    return db.query(Product).all()

@router.get("/products/{product_id}", response_model=Product, tags=["products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get product by ID.
    - **product_id**: Product ID
    - Returns: Product object
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=Product, tags=["products"])
async def update_product(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Update product data.
    - **product_id**: Product ID
    - **product_in**: Updated product data
    - Returns: Updated product object
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}", tags=["products"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete product by ID.
    - **product_id**: Product ID
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

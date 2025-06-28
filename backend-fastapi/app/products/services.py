from sqlalchemy.orm import Session
from typing import List
from app.products.models import Product
from app.products.schemas import ProductCreate

def get_product(db: Session, product_id: int) -> Product:
    """Retrieve a product by ID."""
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session) -> List[Product]:
    """Retrieve all products."""
    return db.query(Product).all()

def create_product(db: Session, product_in: ProductCreate) -> Product:
    """Create a new product."""
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_in: ProductCreate) -> Product:
    """Update an existing product."""
    product = get_product(db, product_id)
    if not product:
        return None
    
    for key, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> None:
    """Delete a product."""
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()

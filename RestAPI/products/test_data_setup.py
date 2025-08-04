"""
Test data setup for products module tests.
Creates necessary test data in the database to support comprehensive testing.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from products.models import DBProduct


def create_test_products():
    """Create test products with various materials configurations"""
    db: Session = SessionLocal()
    
    try:
        # Create test product 1 (already created by shift tests, but ensure it exists)
        product1 = db.query(DBProduct).filter_by(id=1).first()
        if not product1:
            product1 = DBProduct.create_object(
                session=db,
                name="Test Product ABC",
                materials={
                    "steel": {"quantity": 10, "unit": "kg"},
                    "plastic": {"quantity": 2, "unit": "pieces"}
                }
            )
            print("✅ Created test product 1")
        
        # Create test product 2 - Electronics component
        product2 = db.query(DBProduct).filter_by(name="Test Electronics Component").first()
        if not product2:
            product2 = DBProduct.create_object(
                session=db,
                name="Test Electronics Component",
                materials={
                    "copper": {"quantity": 0.5, "unit": "kg"},
                    "silicon": {"quantity": 0.1, "unit": "kg"},
                    "plastic_housing": {"quantity": 1, "unit": "piece"},
                    "screws": {"quantity": 4, "unit": "pieces"}
                }
            )
            print("✅ Created test electronics component")
        
        # Create test product 3 - Simple product with minimal materials
        product3 = db.query(DBProduct).filter_by(name="Simple Test Widget").first()
        if not product3:
            product3 = DBProduct.create_object(
                session=db,
                name="Simple Test Widget",
                materials={
                    "aluminum": {"quantity": 2.5, "unit": "kg"}
                }
            )
            print("✅ Created simple test widget")
        
        # Create test product 4 - Complex product with many materials
        product4 = db.query(DBProduct).filter_by(name="Complex Assembly Unit").first()
        if not product4:
            product4 = DBProduct.create_object(
                session=db,
                name="Complex Assembly Unit",
                materials={
                    "steel_frame": {"quantity": 15, "unit": "kg"},
                    "aluminum_panels": {"quantity": 8, "unit": "pieces"},
                    "bolts_m8": {"quantity": 20, "unit": "pieces"},
                    "bolts_m12": {"quantity": 12, "unit": "pieces"},
                    "rubber_gaskets": {"quantity": 6, "unit": "pieces"},
                    "paint": {"quantity": 0.5, "unit": "liters"},
                    "electrical_cable": {"quantity": 10, "unit": "meters"}
                }
            )
            print("✅ Created complex assembly unit")
        
        # Create test product 5 - Product with no materials (design/service product)
        product5 = db.query(DBProduct).filter_by(name="Design Service Product").first()
        if not product5:
            product5 = DBProduct.create_object(
                session=db,
                name="Design Service Product",
                materials={}
            )
            print("✅ Created design service product")
        
        db.commit()
        print("🎉 All test products created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test products: {e}")
        raise
    finally:
        db.close()


def cleanup_test_products():
    """Clean up test products (optional, for test isolation)"""
    db: Session = SessionLocal()
    
    try:
        test_names = [
            "Test Product ABC",
            "Test Electronics Component", 
            "Simple Test Widget",
            "Complex Assembly Unit",
            "Design Service Product"
        ]
        
        for name in test_names:
            db.query(DBProduct).filter_by(name=name).delete()
        
        db.commit()
        print("🧹 Test products cleaned up")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error cleaning up test products: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_products()
"""
Test data setup for production module tests.
Creates necessary test data in the database to support comprehensive testing.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from production.models import DBProductionOrder, DBProductionOrderItem
from products.models import DBProduct


def create_test_production_orders():
    """Create test production orders and items"""
    db: Session = SessionLocal()
    
    try:
        # Ensure test products exist
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
        
        product2 = db.query(DBProduct).filter_by(name="Test Electronics Component").first()
        if not product2:
            product2 = DBProduct.create_object(
                session=db,
                name="Test Electronics Component",
                materials={
                    "copper": {"quantity": 0.5, "unit": "kg"},
                    "silicon": {"quantity": 0.1, "unit": "kg"}
                }
            )
        
        # Create test production order 1 (already created by shift tests, but ensure it exists)
        prod_order1 = db.query(DBProductionOrder).filter_by(id=1).first()
        if not prod_order1:
            prod_order1 = DBProductionOrder.create_object(
                session=db,
                notes="Test production order for shift testing"
            )
            print("✅ Created test production order 1")
        
        # Create test production order 2 - Electronics batch
        prod_order2 = db.query(DBProductionOrder).filter_by(notes="Electronics production batch").first()
        if not prod_order2:
            prod_order2 = DBProductionOrder.create_object(
                session=db,
                notes="Electronics production batch"
            )
            print("✅ Created electronics production order")
        
        # Create test production order 3 - Mixed products order
        prod_order3 = db.query(DBProductionOrder).filter_by(notes="Mixed products manufacturing order").first()
        if not prod_order3:
            prod_order3 = DBProductionOrder.create_object(
                session=db,
                notes="Mixed products manufacturing order"
            )
            print("✅ Created mixed products production order")
        
        # Create production order items for order 1
        item1 = db.query(DBProductionOrderItem).filter_by(
            production_order_id=prod_order1.id, product_id=product1.id
        ).first()
        if not item1:
            item1 = DBProductionOrderItem.create_object(
                session=db,
                production_order_id=prod_order1.id,
                product_id=product1.id,
                product_amount=50
            )
            print("✅ Created production order item 1")
        
        # Create production order items for order 2
        item2 = db.query(DBProductionOrderItem).filter_by(
            production_order_id=prod_order2.id, product_id=product2.id
        ).first()
        if not item2:
            item2 = DBProductionOrderItem.create_object(
                session=db,
                production_order_id=prod_order2.id,
                product_id=product2.id,
                product_amount=100
            )
            print("✅ Created production order item 2")
        
        # Create multiple items for order 3
        item3 = db.query(DBProductionOrderItem).filter_by(
            production_order_id=prod_order3.id, product_id=product1.id
        ).first()
        if not item3:
            item3 = DBProductionOrderItem.create_object(
                session=db,
                production_order_id=prod_order3.id,
                product_id=product1.id,
                product_amount=25
            )
            print("✅ Created production order item 3a")
        
        item4 = db.query(DBProductionOrderItem).filter_by(
            production_order_id=prod_order3.id, product_id=product2.id
        ).first()
        if not item4:
            item4 = DBProductionOrderItem.create_object(
                session=db,
                production_order_id=prod_order3.id,
                product_id=product2.id,
                product_amount=75
            )
            print("✅ Created production order item 3b")
        
        db.commit()
        print("🎉 All test production orders and items created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test production orders: {e}")
        raise
    finally:
        db.close()


def cleanup_test_production_orders():
    """Clean up test production orders (optional, for test isolation)"""
    db: Session = SessionLocal()
    
    try:
        # Delete production order items first (foreign key constraint)
        db.query(DBProductionOrderItem).delete()
        
        # Delete production orders
        test_notes = [
            "Test production order for shift testing",
            "Electronics production batch",
            "Mixed products manufacturing order"
        ]
        
        for note in test_notes:
            db.query(DBProductionOrder).filter_by(notes=note).delete()
        
        db.commit()
        print("🧹 Test production orders cleaned up")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error cleaning up test production orders: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_production_orders()
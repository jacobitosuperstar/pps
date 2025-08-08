"""
Test data setup for shift module tests.
Creates necessary test data in the database to support comprehensive testing.
"""
from datetime import datetime, date
from sqlalchemy.orm import Session
from database import SessionLocal

# Import all models needed for test data
from employees.models import DBEmployee, RoleChoices
from machines.models import DBMachine, MachineStatus  
from products.models import DBProduct
from production.models import DBProductionOrder
from clients.models import DBClient


def create_test_data():
    """Create all necessary test data for shift tests"""
    db: Session = SessionLocal()
    
    try:
        # Create test client
        test_client = db.query(DBClient).filter_by(identification="TEST_CLIENT").first()
        if not test_client:
            test_client = DBClient.create_object(
                session=db,
                identification="TEST_CLIENT",
                company_name="Test Company Ltd",
                contact_name="Test Contact",
                email="test@testcompany.com",
                phone="+1234567890",
                address="123 Test Street, Test City"
            )
            print("✅ Created test client")
        
        # Create test employee
        test_employee = db.query(DBEmployee).filter_by(identification="TEST_USER").first()
        if not test_employee:
            test_employee = DBEmployee.create_object(
                session=db,
                identification="TEST_USER",
                name="Test User",
                last_name="Employee",
                role=RoleChoices.PRODUCTION,
                salary=50000.0,
                phone="+1234567890",
                email="testuser@company.com",
                hire_date=date(2024, 1, 1)
            )
            print("✅ Created test employee")
        
        # Create test machine
        test_machine = db.query(DBMachine).filter_by(id=1).first()
        if not test_machine:
            test_machine = DBMachine.create_object(
                session=db,
                machine_code="TEST_MACHINE_001",
                name="Test Production Machine",
                status=MachineStatus.ACTIVE,
                location="Production Floor A",
                description="Test machine for automated testing",
                manufacturer="Test Manufacturer",
                model="TM-2024",
                serial_number="TM001-2024",
                installation_date=date(2024, 1, 1)
            )
            print("✅ Created test machine")
        
        # Create test product
        test_product = db.query(DBProduct).filter_by(id=1).first()
        if not test_product:
            test_product = DBProduct.create_object(
                session=db,
                name="Test Product ABC",
                materials={
                    "steel": {"quantity": 10, "unit": "kg"},
                    "plastic": {"quantity": 2, "unit": "pieces"}
                }
            )
            print("✅ Created test product")
        
        # Create test production order
        test_production_order = db.query(DBProductionOrder).filter_by(id=1).first()
        if not test_production_order:
            test_production_order = DBProductionOrder.create_object(
                session=db,
                notes="Test production order for shift testing"
            )
            print("✅ Created test production order")
        
        db.commit()
        print("🎉 All test data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test data: {e}")
        raise
    finally:
        db.close()


def cleanup_test_data():
    """Clean up test data (optional, for test isolation)"""
    db: Session = SessionLocal()
    
    try:
        # Note: Be careful with cleanup in a real environment
        # This is just for testing purposes
        
        # Delete test records (reverse order due to foreign keys)
        db.query(DBProductionOrder).filter_by(id=1).delete()
        db.query(DBProduct).filter_by(id=1).delete()
        db.query(DBMachine).filter_by(id=1).delete()
        db.query(DBEmployee).filter_by(identification="TEST_USER").delete()
        db.query(DBClient).filter_by(identification="TEST_CLIENT").delete()
        
        db.commit()
        print("🧹 Test data cleaned up")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error cleaning up test data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
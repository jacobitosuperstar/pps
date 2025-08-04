"""
Test data setup for employees module tests.
Creates necessary test data in the database to support comprehensive testing.
"""
from datetime import datetime, date
from sqlalchemy.orm import Session
from database import SessionLocal
from employees.models import DBEmployee, RoleChoices


def create_test_employees():
    """Create test employees for various roles and scenarios"""
    db: Session = SessionLocal()
    
    try:
        # Create management employee (already created by shift tests, but let's ensure it exists)
        mgmt_employee = db.query(DBEmployee).filter_by(identification="TEST_MGMT").first()
        if not mgmt_employee:
            mgmt_employee = DBEmployee.create_object(
                session=db,
                identification="TEST_MGMT",
                names="Test Manager",
                last_names="Management",
                role=RoleChoices.MANAGEMENT,
                birthday=date(1980, 1, 1),
                date_joined=date(2024, 1, 1),
                last_login=datetime.now(),
                password="hashed_password_123"
            )
            print("✅ Created test management employee")
        
        # Create HR employee
        hr_employee = db.query(DBEmployee).filter_by(identification="TEST_HR").first()
        if not hr_employee:
            hr_employee = DBEmployee.create_object(
                session=db,
                identification="TEST_HR",
                names="Test HR",
                last_names="Representative",
                role=RoleChoices.HR,
                birthday=date(1985, 5, 15),
                date_joined=date(2024, 2, 1),
                last_login=datetime.now(),
                password="hashed_password_456"
            )
            print("✅ Created test HR employee")
        
        # Create production manager
        prod_mgr = db.query(DBEmployee).filter_by(identification="TEST_PROD_MGR").first()
        if not prod_mgr:
            prod_mgr = DBEmployee.create_object(
                session=db,
                identification="TEST_PROD_MGR",
                names="Test Production",
                last_names="Manager",
                role=RoleChoices.PRODUCTION_MANAGER,
                birthday=date(1978, 8, 20),
                date_joined=date(2024, 1, 15),
                last_login=datetime.now(),
                password="hashed_password_789"
            )
            print("✅ Created test production manager")
        
        # Create production worker
        prod_worker = db.query(DBEmployee).filter_by(identification="TEST_PROD_WORKER").first()
        if not prod_worker:
            prod_worker = DBEmployee.create_object(
                session=db,
                identification="TEST_PROD_WORKER",
                names="Test Production",
                last_names="Worker",
                role=RoleChoices.PRODUCTION,
                birthday=date(1990, 12, 10),
                date_joined=date(2024, 3, 1),
                last_login=datetime.now(),
                password="hashed_password_000"
            )
            print("✅ Created test production worker")
        
        # Create quality employee
        quality_emp = db.query(DBEmployee).filter_by(identification="TEST_QUALITY").first()
        if not quality_emp:
            quality_emp = DBEmployee.create_object(
                session=db,
                identification="TEST_QUALITY",
                names="Test Quality",
                last_names="Inspector",
                role=RoleChoices.QUALITY,
                birthday=date(1987, 3, 25),
                date_joined=date(2024, 2, 15),
                last_login=datetime.now(),
                password="hashed_password_111"
            )
            print("✅ Created test quality employee")
        
        # Ensure the TEST_USER from shift tests exists
        test_user = db.query(DBEmployee).filter_by(identification="TEST_USER").first()
        if not test_user:
            test_user = DBEmployee.create_object(
                session=db,
                identification="TEST_USER",
                names="Test",
                last_names="User",
                role=RoleChoices.PRODUCTION,
                birthday=date(1992, 6, 15),
                date_joined=date(2024, 1, 1),
                last_login=datetime.now(),
                password="hashed_password_test"
            )
            print("✅ Created TEST_USER employee")
        
        db.commit()
        print("🎉 All test employees created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test employees: {e}")
        raise
    finally:
        db.close()


def cleanup_test_employees():
    """Clean up test employees (optional, for test isolation)"""
    db: Session = SessionLocal()
    
    try:
        test_ids = ["TEST_MGMT", "TEST_HR", "TEST_PROD_MGR", "TEST_PROD_WORKER", "TEST_QUALITY"]
        for test_id in test_ids:
            db.query(DBEmployee).filter_by(identification=test_id).delete()
        
        db.commit()
        print("🧹 Test employees cleaned up")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error cleaning up test employees: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_employees()
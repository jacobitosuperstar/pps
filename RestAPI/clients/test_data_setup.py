"""
Test data setup for clients module tests.
Creates necessary test data in the database to support comprehensive testing.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from clients.models import DBClient


def create_test_clients():
    """Create test clients for various scenarios"""
    db: Session = SessionLocal()
    
    try:
        # Create test client 1 (already created by shift tests, but ensure it exists)
        client1 = db.query(DBClient).filter_by(identification="TEST_CLIENT").first()
        if not client1:
            client1 = DBClient.create_object(
                session=db,
                identification="TEST_CLIENT", 
                company_name="Test Company Ltd",
                contact_name="Test Contact",
                email="test@testcompany.com",
                phone="+1234567890",
                address="123 Test Street, Test City"
            )
            print("✅ Created test client 1")
        
        # Create test client 2 - Corporate client
        client2 = db.query(DBClient).filter_by(identification="CORP_CLIENT_001").first()
        if not client2:
            client2 = DBClient.create_object(
                session=db,
                identification="CORP_CLIENT_001",
                company_name="Corporate Solutions Inc",
                contact_name="John Corporate",
                email="john@corporatesolutions.com",
                phone="+1987654321",
                address="456 Business Avenue, Corporate City"
            )
            print("✅ Created corporate client")
        
        # Create test client 3 - Small business client
        client3 = db.query(DBClient).filter_by(identification="SMALL_BIZ_002").first()
        if not client3:
            client3 = DBClient.create_object(
                session=db,
                identification="SMALL_BIZ_002",
                company_name="Small Business Workshop",
                contact_name="Maria Pequeña",
                email="maria@smallbiz.com",
                phone="+1555666777",
                address="789 Small Street, Local Town"
            )
            print("✅ Created small business client")
        
        # Create test client 4 - International client
        client4 = db.query(DBClient).filter_by(identification="INTL_CLIENT_003").first()
        if not client4:
            client4 = DBClient.create_object(
                session=db,
                identification="INTL_CLIENT_003",
                company_name="International Manufacturing Ltd",
                contact_name="Pierre International",
                email="pierre@intlmanufacturing.com",
                phone="+33123456789",
                address="321 International Blvd, Global City"
            )
            print("✅ Created international client")
        
        # Create test client 5 - Government client
        client5 = db.query(DBClient).filter_by(identification="GOV_CLIENT_004").first()
        if not client5:
            client5 = DBClient.create_object(
                session=db,
                identification="GOV_CLIENT_004",
                company_name="Government Agency",
                contact_name="Dr. Official",
                email="official@government.gov",
                phone="+1800555000",
                address="100 Government Plaza, Capital City"
            )
            print("✅ Created government client")
        
        db.commit()
        print("🎉 All test clients created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test clients: {e}")
        raise
    finally:
        db.close()


def cleanup_test_clients():
    """Clean up test clients (optional, for test isolation)"""
    db: Session = SessionLocal()
    
    try:
        test_ids = [
            "TEST_CLIENT",
            "CORP_CLIENT_001", 
            "SMALL_BIZ_002",
            "INTL_CLIENT_003",
            "GOV_CLIENT_004"
        ]
        
        for client_id in test_ids:
            db.query(DBClient).filter_by(identification=client_id).delete()
        
        db.commit()
        print("🧹 Test clients cleaned up")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error cleaning up test clients: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_clients()
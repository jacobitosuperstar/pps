"""
Test data setup for machines module tests.
Creates necessary test data in the database to support comprehensive testing.
"""
from datetime import datetime, date
from sqlalchemy.orm import Session
from database import SessionLocal
from machines.models import (
    DBMachine, MachineStatus, 
    DBMachineMaintenance, MaintenanceType, MaintenanceStatus,
    DBMachineOperator, OperatorSkillLevel
)
from employees.models import DBEmployee, RoleChoices


def create_test_machines():
    """Create test machines and related data"""
    db: Session = SessionLocal()
    
    try:
        # Create test machines
        machine1 = db.query(DBMachine).filter_by(id=1).first()
        if not machine1:
            machine1 = DBMachine.create_object(
                session=db,
                machine_code="TEST_MACHINE_001",
                name="Test Production Machine A",
                status=MachineStatus.ACTIVE,
                location="Production Floor A",
                description="Primary test machine for automated testing",
                manufacturer="Test Manufacturer Inc",
                model="TM-2024-A",
                serial_number="TM001-2024-A",
                installation_date=date(2024, 1, 1)
            )
            print("✅ Created test machine 1")
        
        machine2 = db.query(DBMachine).filter_by(machine_code="TEST_MACHINE_002").first()
        if not machine2:
            machine2 = DBMachine.create_object(
                session=db,
                machine_code="TEST_MACHINE_002", 
                name="Test Production Machine B",
                status=MachineStatus.MAINTENANCE,
                location="Production Floor B",
                description="Secondary test machine for maintenance testing",
                manufacturer="Test Manufacturer Inc",
                model="TM-2024-B",
                serial_number="TM002-2024-B",
                installation_date=date(2024, 2, 1)
            )
            print("✅ Created test machine 2")
        
        machine3 = db.query(DBMachine).filter_by(machine_code="TEST_MACHINE_003").first()
        if not machine3:
            machine3 = DBMachine.create_object(
                session=db,
                machine_code="TEST_MACHINE_003",
                name="Test Assembly Machine",
                status=MachineStatus.INACTIVE,
                location="Assembly Line 1",
                description="Test machine for assembly operations",
                manufacturer="Assembly Corp",
                model="AC-2024",
                serial_number="AC001-2024",
                installation_date=date(2024, 3, 1)
            )
            print("✅ Created test machine 3")
        
        # Ensure test employees exist for operators
        test_employee = db.query(DBEmployee).filter_by(identification="TEST_USER").first()
        if not test_employee:
            test_employee = DBEmployee.create_object(
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
            print("✅ Created TEST_USER for machine operations")
        
        # Create machine operators
        operator1 = db.query(DBMachineOperator).filter_by(
            machine_id=machine1.id, employee_id="TEST_USER"
        ).first()
        if not operator1:
            operator1 = DBMachineOperator.create_object(
                session=db,
                machine_id=machine1.id,
                employee_id="TEST_USER",
                skill_level=OperatorSkillLevel.TRAINED
            )
            print("✅ Created machine operator assignment")
        
        # Create maintenance records
        maintenance1 = db.query(DBMachineMaintenance).filter_by(machine_id=machine1.id).first()
        if not maintenance1:
            maintenance1 = DBMachineMaintenance.create_object(
                session=db,
                machine_id=machine1.id,
                maintenance_type=MaintenanceType.PREVENTIVE,
                status=MaintenanceStatus.SCHEDULED,
                scheduled_date=date(2024, 8, 15),
                description="Routine preventive maintenance",
                estimated_hours=4.0
            )
            print("✅ Created maintenance record")
        
        maintenance2 = db.query(DBMachineMaintenance).filter_by(machine_id=machine2.id).first()
        if not maintenance2:
            maintenance2 = DBMachineMaintenance.create_object(
                session=db,
                machine_id=machine2.id,
                maintenance_type=MaintenanceType.CORRECTIVE,
                status=MaintenanceStatus.IN_PROGRESS,
                scheduled_date=date(2024, 8, 1),
                completed_date=None,
                description="Fix hydraulic system issue",
                estimated_hours=8.0,
                actual_hours=None
            )
            print("✅ Created corrective maintenance record")
        
        db.commit()
        print("🎉 All test machines and related data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating test machines: {e}")
        raise
    finally:
        db.close()


def cleanup_test_machines():
    """Clean up test machines (optional, for test isolation)"""
    db: Session = SessionLocal()
    
    try:
        # Delete in reverse order due to foreign keys
        db.query(DBMachineOperator).filter(
            DBMachineOperator.machine_id.in_([1, 2, 3])
        ).delete(synchronize_session=False)
        
        db.query(DBMachineMaintenance).filter(
            DBMachineMaintenance.machine_id.in_([1, 2, 3])
        ).delete(synchronize_session=False)
        
        db.query(DBMachine).filter(
            DBMachine.machine_code.in_(["TEST_MACHINE_001", "TEST_MACHINE_002", "TEST_MACHINE_003"])
        ).delete(synchronize_session=False)
        
        db.commit()
        print("🧹 Test machines cleaned up")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error cleaning up test machines: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_machines()
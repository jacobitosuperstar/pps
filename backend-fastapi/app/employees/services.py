from sqlalchemy.orm import Session
from typing import List
from app.employees.models import Employee, OOO
from app.employees.schemas import EmployeeCreate, EmployeeUpdate, OOOCreation

def get_employee(db: Session, employee_id: str) -> Employee:
    """Retrieve an employee by ID."""
    return db.query(Employee).filter(Employee.identification == employee_id).first()

def get_employees(db: Session) -> List[Employee]:
    """Retrieve all employees."""
    return db.query(Employee).all()

def create_employee(db: Session, employee_in: EmployeeCreate) -> Employee:
    """Create a new employee."""
    db_employee = Employee(**employee_in.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: str, employee_in: EmployeeUpdate) -> Employee:
    """Update an existing employee."""
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    
    for key, value in employee_in.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: str) -> None:
    """Delete an employee."""
    employee = get_employee(db, employee_id)
    if employee:
        db.delete(employee)
        db.commit()

def create_ooo(db: Session, ooo_in: OOOCreation) -> OOO:
    """Create Out Of Office time for an employee."""
    db_ooo = OOO(
        employee_id=ooo_in.employee_id,
        ooo_type=ooo_in.ooo_type,
        start_date=ooo_in.start_date,
        end_date=ooo_in.end_date,
        description=ooo_in.description
    )
    db.add(db_ooo)
    db.commit()
    db.refresh(db_ooo)
    return db_ooo

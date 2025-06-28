from sqlalchemy.orm import Session
from typing import List, Optional
from app.employees.models import Employee, OOO
from app.employees.schemas import EmployeeCreate, EmployeeUpdate, OOOCreation
from app.core.security import get_password_hash
from fastapi import HTTPException
from fastapi import status

def get_employee(db: Session, employee_id: str) -> Optional[Employee]:
    """Retrieve an employee by ID."""
    return db.query(Employee).filter(Employee.identification == employee_id).first()

def get_employees(db: Session) -> List[Employee]:
    """Retrieve all employees."""
    return db.query(Employee).all()

def create_employee(db: Session, employee_in: EmployeeCreate) -> Employee:
    """Create a new employee.
    
    Args:
        db: Database session
        employee_in: Employee data
        
    Returns:
        Employee: The created employee
        
    Raises:
        HTTPException: If employee with the same ID already exists
    """
    from datetime import date
    
    # Verificar si el empleado ya existe
    db_employee = get_employee(db, employee_in.identification)
    if db_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Employee with ID {employee_in.identification} already exists"
        )
    
    # Obtener los datos del empleado y encriptar la contraseña
    employee_data = employee_in.model_dump()
    if 'password' in employee_data and employee_data['password']:
        employee_data['password'] = get_password_hash(employee_data['password'])
    
    # Establecer valores por defecto para los campos requeridos
    employee_data.update({
        'date_joined': date.today(),
        'last_login': date.today(),
        'is_active': True,
        'is_staff': False,
        'is_superuser': False
    })
    
    db_employee = Employee(**employee_data)
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

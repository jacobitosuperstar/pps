from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.employees import Employee, OOO
from app.schemas.employees import EmployeeCreate, EmployeeUpdate, Employee, OOOCreation, OOOUpdate

router = APIRouter()

@router.post("/employees/", response_model=Employee, tags=["employees"])
async def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee.
    - **employee_in**: Employee data to create
    - Returns: Created employee object
    """
    db_employee = Employee(**employee_in.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/", response_model=List[Employee], tags=["employees"])
async def get_employees(db: Session = Depends(get_db)):
    """
    Get all employees.
    - Returns: List of all employees
    """
    return db.query(Employee).all()

@router.get("/employees/{employee_id}", response_model=Employee, tags=["employees"])
async def get_employee(employee_id: str, db: Session = Depends(get_db)):
    """
    Get employee by ID.
    - **employee_id**: Employee identification
    - Returns: Employee object
    """
    employee = db.query(Employee).filter(Employee.identification == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{employee_id}", response_model=Employee, tags=["employees"])
async def update_employee(employee_id: str, employee_in: EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update employee data.
    - **employee_id**: Employee identification
    - **employee_in**: Updated employee data
    - Returns: Updated employee object
    """
    employee = db.query(Employee).filter(Employee.identification == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee_in.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)
    
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/employees/{employee_id}", tags=["employees"])
async def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    """
    Delete employee by ID.
    - **employee_id**: Employee identification
    """
    employee = db.query(Employee).filter(Employee.identification == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

@router.post("/employees/{employee_id}/ooo", response_model=OOOUpdate, tags=["employees"])
async def create_ooo(employee_id: str, ooo_in: OOOCreation, db: Session = Depends(get_db)):
    """
    Create Out Of Office time for an employee.
    - **employee_id**: Employee identification
    - **ooo_in**: OOO data to create
    - Returns: Created OOO object
    """
    employee = db.query(Employee).filter(Employee.identification == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_ooo = OOO(
        employee_id=employee_id,
        ooo_type=ooo_in.ooo_type,
        start_date=ooo_in.start_date,
        end_date=ooo_in.end_date,
        description=ooo_in.description
    )
    db.add(db_ooo)
    db.commit()
    db.refresh(db_ooo)
    return db_ooo

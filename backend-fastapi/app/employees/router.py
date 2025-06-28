from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.employees.models import Employee
from app.employees.schemas import EmployeeCreate, EmployeeUpdate, Employee, OOOCreation, OOOUpdate
from app.employees.services import (
    get_employee,
    get_employees,
    create_employee,
    update_employee,
    delete_employee,
    create_ooo
)
from typing import List

router = APIRouter()

@router.post("/employees/", response_model=Employee, tags=["employees"])
async def create_employee_endpoint(employee_in: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee.
    - **employee_in**: Employee data to create
    - Returns: Created employee object
    """
    return create_employee(db, employee_in)

@router.get("/employees/", response_model=List[Employee], tags=["employees"])
async def get_employees_endpoint(db: Session = Depends(get_db)):
    """
    Get all employees.
    - Returns: List of all employees
    """
    return get_employees(db)

@router.get("/employees/{employee_id}", response_model=Employee, tags=["employees"])
async def get_employee_endpoint(employee_id: str, db: Session = Depends(get_db)):
    """
    Get employee by ID.
    - **employee_id**: Employee identification
    - Returns: Employee object
    """
    employee = get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{employee_id}", response_model=Employee, tags=["employees"])
async def update_employee_endpoint(employee_id: str, employee_in: EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update employee data.
    - **employee_id**: Employee identification
    - **employee_in**: Updated employee data
    - Returns: Updated employee object
    """
    employee = update_employee(db, employee_id, employee_in)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.delete("/employees/{employee_id}", tags=["employees"])
async def delete_employee_endpoint(employee_id: str, db: Session = Depends(get_db)):
    """
    Delete employee by ID.
    - **employee_id**: Employee identification
    """
    delete_employee(db, employee_id)
    return {"message": "Employee deleted successfully"}

@router.post("/employees/{employee_id}/ooo", response_model=OOOUpdate, tags=["employees"])
async def create_ooo_endpoint(employee_id: str, ooo_in: OOOCreation, db: Session = Depends(get_db)):
    """
    Create Out Of Office time for an employee.
    - **employee_id**: Employee identification
    - **ooo_in**: OOO data to create
    - Returns: Created OOO object
    """
    return create_ooo(db, ooo_in)

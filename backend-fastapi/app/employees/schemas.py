from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional, List

class EmployeeBase(BaseModel):
    names: str = Field(..., min_length=1, max_length=100)
    last_names: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=20)
    birthday: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    identification: str = Field(..., min_length=1, max_length=50)
    password: Optional[str] = None

class EmployeeUpdate(EmployeeBase):
    identification: Optional[str] = None
    password: Optional[str] = None

class Employee(EmployeeBase):
    identification: str
    date_joined: date
    last_login: date
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class OOOCreation(BaseModel):
    employee_id: str
    ooo_type: str = Field(..., min_length=1, max_length=20)
    start_date: date
    end_date: date
    description: Optional[str] = None

class OOOUpdate(OOOCreation):
    id: int

    class Config:
        from_attributes = True

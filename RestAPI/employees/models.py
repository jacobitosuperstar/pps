from typing import Optional
from datetime import date, datetime
from enum import Enum

from sqlalchemy import Column, String, Date, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict

from base.models import Base, PaginatedElements


class DBEmployee(Base):
    __tablename__: str = "employees"

    identification = Column(
        String(50),
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )
    names = Column(
        String(100),
        nullable=False,
    )
    last_names = Column(
        String(100),
        nullable=False,
    )
    role = Column(
        String(20),
        nullable=False,
    )
    birthday = Column(
        Date,
        nullable=True,
    )
    date_joined = Column(
        Date,
        nullable=False,
    )
    last_login = Column(
        DateTime,
        nullable=False,
    )
    password = Column(
        String(128),
        nullable=True,
    )

    ooos = relationship(
        "DBOOO",
        back_populates="employee",
    )


class RoleChoices(str, Enum):
    MANAGEMENT = "management"
    HR = "hr"
    QUALITY = "quality"
    PRODUCTION_MANAGER = "prod_manager"
    PRODUCTION = "prod"
    ACCOUNTING = "accounting"


class EmployeeBase(BaseModel):
    identification: str = Field(..., max_length=50)
    names: str = Field(..., max_length=100)
    last_names: str = Field(..., max_length=100)
    role: RoleChoices = Field(...)
    birthday: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    password: Optional[str] = None


class EmployeeRead(EmployeeBase):
    date_joined: date
    last_login: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeUpdate(BaseModel):
    names: Optional[str] = None
    last_names: Optional[str] = None
    role: Optional[RoleChoices] = None
    birthday: Optional[date] = None
    password: Optional[str] = None


class EmployeeLogin(BaseModel):
    identification: str
    password: str


PaginatedEmployees = PaginatedElements[EmployeeRead]


class DBOOO(Base):
    __tablename__ = "ooo"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    employee_id = Column(
        String(50),
        ForeignKey("employees.identification"),
        nullable=False,
    )
    ooo_type = Column(
        String(20),
        nullable=False,
    )
    start_date = Column(
        DateTime,
        nullable=False,
    )
    end_date = Column(
        DateTime,
        nullable=False,
    )
    description = Column(
        String,
        nullable=False,
    )

    employee = relationship(
        "DBEmployee",
        back_populates="ooos",
    )


class OOOTypes(str, Enum):
    PL = "paid_leave"
    NPL = "non_paid_leave"
    WA = "work_accident"
    NWA = "non_work_accident"
    PP = "paid_permit"
    NPP = "non_paid_permit"


class OOOCreation(BaseModel):
    employee_id: str
    ooo_type: OOOTypes
    start_date: datetime
    end_date: datetime
    description: str


class OOOUpdate(BaseModel):
    ooo_type: Optional[OOOTypes] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class OOORead(OOOCreation):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


PaginatedOOOs = PaginatedElements[OOORead]

from typing import Optional
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict

from base.models import Base, PaginatedElements
from employees.models import EmployeeRead
from machines.models import MachineRead
from production.models import ProductionOrderRead
from products.models import ProductRead

class ShiftType(str, Enum):
    PRODUCTION = "production"
    MAINTENANCE = "maintenance"
    MACHINE_BROKEN = "machine_broken"
    SETUP = "setup"
    CLEANING = "cleaning"
    INSPECTION = "inspection"
    TRAINING = "training"
    OTHER = "other"


class ShiftStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class DBShift(Base):
    """Shift assignments that link machines, employees, and production orders."""
    __tablename__ = "shifts"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    machine_id = Column(
        Integer,
        ForeignKey("machines.id"),
        nullable=False,
    )
    employee_id = Column(
        String(50),
        ForeignKey("employees.identification"),
        nullable=False,
    )
    production_order_id = Column(
        Integer,
        ForeignKey("production_orders.id"),
        nullable=True,  # Optional for maintenance, training, etc.
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=True,  # Only required for production shifts
    )
    shift_type = Column(
        String(20),
        nullable=False,
    )
    status = Column(
        String(20),
        nullable=False,
        default=ShiftStatus.SCHEDULED.value,
    )
    start_datetime = Column(
        DateTime,
        nullable=False,
    )
    end_datetime = Column(
        DateTime,
        nullable=False,
    )
    production_code = Column(
        String(100),
        nullable=True,
        index=True,
    )
    description = Column(
        String(200),
        nullable=False,
    )
    notes = Column(
        Text,
        nullable=True,
    )

    # Relationships
    machine = relationship("DBMachine")
    employee = relationship("DBEmployee")
    production_order = relationship("DBProductionOrder")
    product = relationship("DBProduct")


class Shift(BaseModel):
    machine_id: int = Field(..., description="Machine ID")
    employee_id: str = Field(..., description="Employee ID (operator)")
    production_order_id: Optional[int] = Field(None, description="Production order ID (optional)")
    product_id: Optional[int] = Field(None, description="Product ID (required for production shifts)")
    shift_type: ShiftType = Field(..., description="Type of shift")
    status: ShiftStatus = Field(ShiftStatus.SCHEDULED, description="Shift status")
    start_datetime: datetime = Field(..., description="Start datetime (ISO format)")
    end_datetime: datetime = Field(..., description="End datetime (ISO format)")
    description: str = Field(..., description="Shift description")
    notes: Optional[str] = Field(None, description="Additional notes")


class ShiftUpdate(BaseModel):
    production_order_id: Optional[int] = Field(None, description="Production order ID")
    product_id: Optional[int] = Field(None, description="Product ID")
    shift_type: Optional[ShiftType] = Field(None, description="Type of shift")
    status: Optional[ShiftStatus] = Field(None, description="Shift status")
    start_datetime: Optional[datetime] = Field(None, description="Start datetime (ISO format)")
    end_datetime: Optional[datetime] = Field(None, description="End datetime (ISO format)")
    description: Optional[str] = Field(None, description="Shift description")
    notes: Optional[str] = Field(None, description="Additional notes")


class ShiftRead(Shift):
    id: int
    production_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted: bool
    machine: Optional[MachineRead] = None
    employee: Optional[EmployeeRead] = None
    production_order: Optional[ProductionOrderRead] = None
    product: Optional[ProductRead] = None

    model_config = ConfigDict(from_attributes=True)


PaginatedShifts = PaginatedElements[ShiftRead]

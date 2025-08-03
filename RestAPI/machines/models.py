from typing import Optional, List
from datetime import datetime, date
from enum import Enum

from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict

from base.models import Base, PaginatedElements
from employees.models import EmployeeRead


# ============================================================================
# MACHINE MODELS
# ============================================================================

class MachineStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"
    RETIRED = "retired"


class DBMachine(Base):
    """
    Physical machines in the plant.

    Attributes:
        id: Unique identifier for the machine.
        machine_code: Machine code/identifier.
        name: Machine name.
        status: Current status (active, maintenance, inactive, retired).
        location: Physical location in the plant.
        description: Machine description.
        manufacturer: Machine manufacturer.
        model: Machine model.
        serial_number: Machine serial number.
        installation_date: When the machine was installed.
        created_at: When the record was created.
        updated_at: When the record was last updated.
        deleted: Soft delete flag.
    """
    __tablename__ = "machines"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
    )
    machine_code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(
        String(100),
        nullable=False,
    )
    status = Column(
        String(20),
        nullable=False,
        default=MachineStatus.ACTIVE.value,
    )
    location = Column(
        String(100),
        nullable=True,
    )
    description = Column(
        Text,
        nullable=True,
    )
    manufacturer = Column(
        String(100),
        nullable=True,
    )
    model = Column(
        String(100),
        nullable=True,
    )
    serial_number = Column(
        String(100),
        nullable=True,
    )
    installation_date = Column(
        Date,
        nullable=True,
    )

    # Relationships
    operators = relationship("DBMachineOperator", back_populates="machine", cascade="all, delete-orphan")
    maintenance_records = relationship("DBMachineMaintenance", back_populates="machine", cascade="all, delete-orphan")


class Machine(BaseModel):
    machine_code: str = Field(..., description="Machine code/identifier")
    name: str = Field(..., description="Machine name")
    status: MachineStatus = Field(MachineStatus.ACTIVE, description="Current status")
    location: Optional[str] = Field(None, description="Physical location in the plant")
    description: Optional[str] = Field(None, description="Machine description")
    manufacturer: Optional[str] = Field(None, description="Machine manufacturer")
    model: Optional[str] = Field(None, description="Machine model")
    serial_number: Optional[str] = Field(None, description="Machine serial number")
    installation_date: Optional[date] = Field(None, description="Installation date")


class MachineUpdate(BaseModel):
    machine_code: Optional[str] = Field(None, description="Machine code/identifier")
    name: Optional[str] = Field(None, description="Machine name")
    status: Optional[MachineStatus] = Field(None, description="Current status")
    location: Optional[str] = Field(None, description="Physical location in the plant")
    description: Optional[str] = Field(None, description="Machine description")
    manufacturer: Optional[str] = Field(None, description="Machine manufacturer")
    model: Optional[str] = Field(None, description="Machine model")
    serial_number: Optional[str] = Field(None, description="Machine serial number")
    installation_date: Optional[date] = Field(None, description="Installation date")


class MachineRead(Machine):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool
    operators: List["MachineOperatorRead"] = []
    maintenance_records: List["MachineMaintenanceRead"] = []

    model_config = ConfigDict(from_attributes=True)


PaginatedMachines = PaginatedElements[MachineRead]


# ============================================================================
# MACHINE MAINTENANCE MODELS
# ============================================================================

class MaintenanceType(str, Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    EMERGENCY = "emergency"
    INSPECTION = "inspection"


class MaintenanceStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class DBMachineMaintenance(Base):
    """
    Maintenance records for machines.

    Attributes:
        id: Unique identifier for the maintenance record.
        machine_id: Foreign key to the machine.
        maintenance_type: Type of maintenance (preventive, corrective, etc.).
        status: Current status of the maintenance.
        scheduled_date: When the maintenance was scheduled.
        actual_date: When the maintenance was actually performed.
        cost: Cost of the maintenance.
        description: Description of the maintenance work.
        work_performed: Detailed description of work performed.
        next_maintenance_date: Proposed date for next maintenance.
        created_at: When the record was created.
        updated_at: When the record was last updated.
        deleted: Soft delete flag.
    """
    __tablename__ = "machine_maintenance"

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
    maintenance_type = Column(
        String(20),
        nullable=False,
    )
    status = Column(
        String(20),
        nullable=False,
        default=MaintenanceStatus.SCHEDULED.value,
    )
    scheduled_date = Column(
        Date,
        nullable=False,
    )
    actual_date = Column(
        Date,
        nullable=True,
    )
    cost = Column(
        Float,
        nullable=True,
    )
    description = Column(
        String(200),
        nullable=False,
    )
    work_performed = Column(
        Text,
        nullable=True,
    )
    next_maintenance_date = Column(
        Date,
        nullable=True,
    )

    # Relationships
    machine = relationship("DBMachine", back_populates="maintenance_records")


class MachineMaintenance(BaseModel):
    machine_id: int = Field(..., description="Machine ID")
    maintenance_type: MaintenanceType = Field(..., description="Type of maintenance")
    status: MaintenanceStatus = Field(MaintenanceStatus.SCHEDULED, description="Maintenance status")
    scheduled_date: date = Field(..., description="Scheduled maintenance date")
    actual_date: Optional[date] = Field(None, description="Actual maintenance date")
    cost: Optional[float] = Field(None, description="Maintenance cost")
    description: str = Field(..., description="Maintenance description")
    work_performed: Optional[str] = Field(None, description="Detailed work performed")
    next_maintenance_date: Optional[date] = Field(None, description="Proposed next maintenance date")


class MachineMaintenanceUpdate(BaseModel):
    maintenance_type: Optional[MaintenanceType] = Field(None, description="Type of maintenance")
    status: Optional[MaintenanceStatus] = Field(None, description="Maintenance status")
    scheduled_date: Optional[date] = Field(None, description="Scheduled maintenance date")
    actual_date: Optional[date] = Field(None, description="Actual maintenance date")
    cost: Optional[float] = Field(None, description="Maintenance cost")
    description: Optional[str] = Field(None, description="Maintenance description")
    work_performed: Optional[str] = Field(None, description="Detailed work performed")
    next_maintenance_date: Optional[date] = Field(None, description="Proposed next maintenance date")


class MachineMaintenanceRead(MachineMaintenance):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


PaginatedMachineMaintenance = PaginatedElements[MachineMaintenanceRead]


# ============================================================================
# MACHINE OPERATOR RELATIONSHIP MODELS
# ============================================================================

class OperatorSkillLevel(str, Enum):
    TRAINED = "trained"      # Fully trained operator
    TRAINEE = "trainee"      # Learning to operate


class DBMachineOperator(Base):
    """
    Relationship between machines and operators (employees who can operate them).

    Attributes:
        id: Unique identifier for the relationship.
        machine_id: Foreign key to the machine.
        employee_id: Foreign key to the employee.
        skill_level: Operator's skill level for this machine.
        created_at: When the record was created.
        updated_at: When the record was last updated.
        deleted: Soft delete flag.
    """
    __tablename__ = "machine_operators"

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
    skill_level = Column(
        String(20),
        nullable=False,
        default=OperatorSkillLevel.TRAINEE.value,
    )

    # Relationships
    machine = relationship("DBMachine", back_populates="operators")
    employee = relationship("DBEmployee")


class MachineOperator(BaseModel):
    machine_id: int = Field(..., description="Machine ID")
    employee_id: str = Field(..., description="Employee ID")
    skill_level: OperatorSkillLevel = Field(OperatorSkillLevel.TRAINEE, description="Operator's skill level")


class MachineOperatorUpdate(BaseModel):
    skill_level: Optional[OperatorSkillLevel] = Field(None, description="Operator's skill level")


class MachineOperatorRead(MachineOperator):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool
    employee: EmployeeRead

    model_config = ConfigDict(from_attributes=True)


PaginatedMachineOperators = PaginatedElements[MachineOperatorRead]

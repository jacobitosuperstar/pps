from sqlalchemy import Column, String, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class ExistingMachineTypes:
    PI = "plastic_inyector"
    PE = "plastic_extruder"

    choices = [
        (PI, "Plastic Inyector"),
        (PE, "Plastic Extruder")
    ]

class MachineType(Base):
    __tablename__ = "machine_types"

    id = Column(Integer, primary_key=True, index=True)
    machine_type = Column(String(100), nullable=False, unique=True)

    # Relación many-to-many con Employee a través de la tabla de asociación
    trained_employees = relationship("Employee", secondary="employee_machines")

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_number = Column(String(100), nullable=False)
    machine_title = Column(String(100), nullable=False)
    machine_type_id = Column(Integer, ForeignKey("machine_types.id"))

    machine_type = relationship("MachineType", backref="machines")

    __table_args__ = (
        UniqueConstraint("machine_number", "machine_title"),
    )

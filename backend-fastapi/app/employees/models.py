from sqlalchemy import Column, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class RoleChoices:
    MANAGEMENT = "management"
    HR = "hr"
    QUALITY = "quality"
    PRODUCTION_MANAGER = "prod_manager"
    PRODUCTION = "prod"
    ACCOUNTING = "accounting"

    choices = [
        (MANAGEMENT, "Management"),
        (HR, "Human Resources"),
        (QUALITY, "Quality"),
        (PRODUCTION_MANAGER, "Production Manager"),
        (PRODUCTION, "Production"),
        (ACCOUNTING, "Accounting")
    ]

class Employee(Base):
    __tablename__ = "employees"

    identification = Column(String(50), primary_key=True)
    names = Column(String(100), nullable=False)
    last_names = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=True)
    date_joined = Column(Date, nullable=False)
    last_login = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    trained_machines = relationship("MachineType", secondary="employee_machines")

class OOO(Base):
    __tablename__ = "ooos"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), ForeignKey("employees.identification"))
    ooo_type = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)

    employee = relationship("Employee", backref="ooos")

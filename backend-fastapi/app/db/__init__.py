from .base import Base
from .session import engine, SessionLocal

# Importar todos los modelos para que se registren
from app.employees.models import Employee, OOO
from app.machines.models import MachineType, Machine
from app.clients.models import Client
from app.production.models import SaleOrder, ProductionOrder, QualityEvaluation
from app.products.models import Product

__all__ = ["Base", "engine", "SessionLocal"]

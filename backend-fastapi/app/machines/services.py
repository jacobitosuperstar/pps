from sqlalchemy.orm import Session
from typing import List
from app.machines.models import MachineType, Machine
from app.machines.schemas import MachineTypeCreate, MachineCreate

def get_machine_type(db: Session, type_id: int) -> MachineType:
    """Retrieve a machine type by ID."""
    return db.query(MachineType).filter(MachineType.id == type_id).first()

def get_machine_types(db: Session) -> List[MachineType]:
    """Retrieve all machine types."""
    return db.query(MachineType).all()

def create_machine_type(db: Session, type_in: MachineTypeCreate) -> MachineType:
    """Create a new machine type."""
    db_type = MachineType(**type_in.model_dump())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def get_machine(db: Session, machine_id: int) -> Machine:
    """Retrieve a machine by ID."""
    return db.query(Machine).filter(Machine.id == machine_id).first()

def get_machines(db: Session) -> List[Machine]:
    """Retrieve all machines."""
    return db.query(Machine).all()

def create_machine(db: Session, machine_in: MachineCreate) -> Machine:
    """Create a new machine."""
    db_machine = Machine(**machine_in.model_dump())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

def update_machine(db: Session, machine_id: int, machine_in: MachineCreate) -> Machine:
    """Update an existing machine."""
    machine = get_machine(db, machine_id)
    if not machine:
        return None
    
    for key, value in machine_in.model_dump(exclude_unset=True).items():
        setattr(machine, key, value)
    
    db.commit()
    db.refresh(machine)
    return machine

def delete_machine(db: Session, machine_id: int) -> None:
    """Delete a machine."""
    machine = get_machine(db, machine_id)
    if machine:
        db.delete(machine)
        db.commit()

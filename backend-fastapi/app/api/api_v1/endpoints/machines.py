from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.machines import MachineType, Machine
from app.schemas.machines import MachineTypeCreate, MachineType, MachineCreate, Machine

router = APIRouter()

@router.post("/machine-types/", response_model=MachineType, tags=["machines"])
async def create_machine_type(machine_type_in: MachineTypeCreate, db: Session = Depends(get_db)):
    """
    Create a new machine type.
    - **machine_type_in**: Machine type data to create
    - Returns: Created machine type object
    """
    db_machine_type = MachineType(**machine_type_in.model_dump())
    db.add(db_machine_type)
    db.commit()
    db.refresh(db_machine_type)
    return db_machine_type

@router.get("/machine-types/", response_model=List[MachineType], tags=["machines"])
async def get_machine_types(db: Session = Depends(get_db)):
    """
    Get all machine types.
    - Returns: List of all machine types
    """
    return db.query(MachineType).all()

@router.get("/machines/", response_model=List[Machine], tags=["machines"])
async def get_machines(db: Session = Depends(get_db)):
    """
    Get all machines.
    - Returns: List of all machines
    """
    return db.query(Machine).all()

@router.post("/machines/", response_model=Machine, tags=["machines"])
async def create_machine(machine_in: MachineCreate, db: Session = Depends(get_db)):
    """
    Create a new machine.
    - **machine_in**: Machine data to create
    - Returns: Created machine object
    """
    db_machine = Machine(**machine_in.model_dump())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

@router.get("/machines/{machine_id}", response_model=Machine, tags=["machines"])
async def get_machine(machine_id: int, db: Session = Depends(get_db)):
    """
    Get machine by ID.
    - **machine_id**: Machine ID
    - Returns: Machine object
    """
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.put("/machines/{machine_id}", response_model=Machine, tags=["machines"])
async def update_machine(machine_id: int, machine_in: MachineCreate, db: Session = Depends(get_db)):
    """
    Update machine data.
    - **machine_id**: Machine ID
    - **machine_in**: Updated machine data
    - Returns: Updated machine object
    """
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    for key, value in machine_in.model_dump(exclude_unset=True).items():
        setattr(machine, key, value)
    
    db.commit()
    db.refresh(machine)
    return machine

@router.delete("/machines/{machine_id}", tags=["machines"])
async def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    """
    Delete machine by ID.
    - **machine_id**: Machine ID
    """
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    db.delete(machine)
    db.commit()
    return {"message": "Machine deleted successfully"}

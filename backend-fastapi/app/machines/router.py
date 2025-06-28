from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.machines.models import MachineType, Machine
from app.machines.schemas import MachineTypeCreate, MachineCreate, MachineType, Machine
from app.machines.services import (
    get_machine_type,
    get_machine_types,
    create_machine_type,
    get_machine,
    get_machines,
    create_machine,
    update_machine,
    delete_machine
)
from typing import List

router = APIRouter()

@router.post("/machine-types/", response_model=MachineType, tags=["machines"])
async def create_machine_type_endpoint(type_in: MachineTypeCreate, db: Session = Depends(get_db)):
    """
    Create a new machine type.
    - **type_in**: Machine type data to create
    - Returns: Created machine type object
    """
    return create_machine_type(db, type_in)

@router.get("/machine-types/", response_model=List[MachineType], tags=["machines"])
async def get_machine_types_endpoint(db: Session = Depends(get_db)):
    """
    Get all machine types.
    - Returns: List of all machine types
    """
    return get_machine_types(db)

@router.get("/machines/", response_model=List[Machine], tags=["machines"])
async def get_machines_endpoint(db: Session = Depends(get_db)):
    """
    Get all machines.
    - Returns: List of all machines
    """
    return get_machines(db)

@router.post("/machines/", response_model=Machine, tags=["machines"])
async def create_machine_endpoint(machine_in: MachineCreate, db: Session = Depends(get_db)):
    """
    Create a new machine.
    - **machine_in**: Machine data to create
    - Returns: Created machine object
    """
    return create_machine(db, machine_in)

@router.get("/machines/{machine_id}", response_model=Machine, tags=["machines"])
async def get_machine_endpoint(machine_id: int, db: Session = Depends(get_db)):
    """
    Get machine by ID.
    - **machine_id**: Machine ID
    - Returns: Machine object
    """
    machine = get_machine(db, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.put("/machines/{machine_id}", response_model=Machine, tags=["machines"])
async def update_machine_endpoint(machine_id: int, machine_in: MachineCreate, db: Session = Depends(get_db)):
    """
    Update machine data.
    - **machine_id**: Machine ID
    - **machine_in**: Updated machine data
    - Returns: Updated machine object
    """
    machine = update_machine(db, machine_id, machine_in)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.delete("/machines/{machine_id}", tags=["machines"])
async def delete_machine_endpoint(machine_id: int, db: Session = Depends(get_db)):
    """
    Delete machine by ID.
    - **machine_id**: Machine ID
    """
    delete_machine(db, machine_id)
    return {"message": "Machine deleted successfully"}

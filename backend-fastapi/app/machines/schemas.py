from pydantic import BaseModel, Field
from typing import Optional

class MachineTypeBase(BaseModel):
    machine_type: str = Field(..., min_length=1, max_length=100)

class MachineTypeCreate(MachineTypeBase):
    pass

class MachineType(MachineTypeBase):
    id: int

    class Config:
        from_attributes = True

class MachineBase(BaseModel):
    machine_number: str = Field(..., min_length=1, max_length=100)
    machine_title: str = Field(..., min_length=1, max_length=100)
    machine_type_id: int

class MachineCreate(MachineBase):
    pass

class Machine(MachineBase):
    id: int

    class Config:
        from_attributes = True

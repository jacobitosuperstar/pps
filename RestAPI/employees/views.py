from typing import List
from fastapi import APIRouter, HTTPException
from . import models


router: APIRouter = APIRouter(
    prefix="/employees",
    tags=["employees"],
)



@router.get("/")
def get_employees() -> List[models.Employee]:
    """
    """
    ...

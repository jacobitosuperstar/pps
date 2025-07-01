from typing import List, Optional, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import Response
from .models import (
    RoleChoices,
    DBEmployee,
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
    EmployeeLogin,
    PaginatedEmployees,
    DBOOO,
    OOOTypes,
    OOOCreation,
    OOOUpdate,
    OOORead,
    PaginatedOOOs,
)
from jwt_authentication.decorators import get_current_user
from jwt_authentication.jwt_authentication import create_token
from sqlalchemy.orm import Session
from database import get_session
from datetime import datetime, date, UTC
from .utils import require_roles
from base.db_base_services import filter_instances


router: APIRouter = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


# --- Login Endpoint ---
@router.post("/login")
def login(
    payload: EmployeeLogin,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    emp: Optional[DBEmployee] = session.query(
        DBEmployee
    ).filter_by(
        identification=payload.identification
    ).first()

    if not emp or emp.password != payload.password or emp.role == RoleChoices.PRODUCTION.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_token(
        employee_id=emp.identification,
        employee_role=emp.role
    )
    emp.update_instance(
        session=session,
        **{"last_login": datetime.now(UTC)},
    )
    return {
        "response": "Logged in successfully",
        "employee": EmployeeRead.model_validate(emp),
        "token": token
    }


# --- List Employees ---
@router.get(
    "/",
    response_model=PaginatedEmployees,
)
def list_employees(
    identification: Optional[str] = None,
    names: Optional[str] = None,
    last_names: Optional[str] = None,
    role: Optional[RoleChoices] = None,
    birthday: Optional[date] = None,
    is_active: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedEmployees:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    filters: dict = {
        "identification": identification,
        "names": names,
        "last_names": last_names,
        "role": role,
        "birthday": birthday,
        "is_active": is_active,
    }
    filters: dict = {k: v for k, v in filters.items() if v is not None}
    employees, total_count = filter_instances(
        model=DBEmployee,
        session=session,
        filters=filters,
        limit=limit,
        offset=offset,
    )
    results: List[EmployeeRead] = [EmployeeRead.model_validate(e) for e in employees]
    return PaginatedEmployees(results=results, total_count=total_count)


# --- Create Employee (HR/Management only) ---
@router.post(
    "/",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    payload: EmployeeCreate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBEmployee:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    emp: DBEmployee = DBEmployee.create_object(
        session,
        date_joined=datetime.now().date(),
        last_login=datetime.now(),
        **payload.model_dump(),
    )
    return emp


# --- Get Employee by Identification ---
@router.get(
    "/{identification}",
    response_model=EmployeeRead,
)
def get_employee(
    identification: str,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBEmployee:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    emp: Optional[DBEmployee] = session.query(
        DBEmployee
    ).filter_by(
        identification=identification
    ).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp


# --- Update Employee (HR/Management only) ---
@router.put(
    "/{identification}",
    response_model=EmployeeRead,
)
def update_employee(
    identification: str,
    payload: EmployeeUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBEmployee:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    emp: Optional[DBEmployee] = session.query(
        DBEmployee
    ).filter_by(
        identification=identification
    ).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    update_data: dict = payload.model_dump(exclude_unset=True)
    emp.update_instance(session, **update_data)
    return emp

# --- Delete Employee (HR/Management only, soft delete) ---
@router.delete("/{identification}")
def delete_employee(
    identification: str,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    emp = session.query(DBEmployee).filter_by(identification=identification).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    emp.delete_instance(session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/roles")
def get_roles() -> dict:
    return {
            role.value: role.name.replace('_', ' ').title()
            for role in RoleChoices
    }

@router.get("/ooo_types")
def get_ooo_types() -> dict:
    return {
        ooo.value: ooo.name.replace('_', ' ').title()
        for ooo in OOOTypes
    }

# --- List OOO ---
@router.get(
    "/ooo/",
    response_model=PaginatedOOOs,
)
def list_ooo(
    employee_id: Optional[str] = None,
    ooo_type: Optional[OOOTypes] = None,
    is_deleted: Optional[bool] = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedOOOs:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    filters = {
        "employee_id": employee_id,
        "ooo_type": ooo_type,
        "is_deleted": is_deleted,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    ooos, total_count = filter_instances(DBOOO, session, filters, limit=limit, offset=offset)
    results = [OOORead.model_validate(o) for o in ooos]
    return PaginatedOOOs(results=results, total_count=total_count)

# --- Create OOO ---
@router.post(
    "/ooo/",
    response_model=OOORead,
    status_code=status.HTTP_201_CREATED
)
def create_ooo(
    payload: OOOCreation,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBOOO:
    require_roles(token, [RoleChoices.HR])
    ooo: DBOOO = DBOOO.create_object(
        session=session,
        **payload.model_dump(),
    )
    return ooo

# --- Get OOO by ID ---
@router.get(
    "/ooo/{id}",
    response_model=OOORead,
)
def get_ooo(
    id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBOOO:
    require_roles(
        token,
        [
            RoleChoices.HR,
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
        ]
    )
    ooo: Optional[DBOOO] = session.query(
        DBOOO
    ).filter_by(
        id=id
    ).first()
    if not ooo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OOO not found")
    return ooo

# --- Update OOO ---
@router.post(
    "/ooo/{id}",
    response_model=OOORead,
)
def update_ooo(
    id: int,
    payload: OOOUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBOOO:
    require_roles(token, [RoleChoices.HR])
    ooo: Optional[DBOOO] = session.query(
        DBOOO
    ).filter_by(
        id=id
    ).first()
    if not ooo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OOO not found")
    ooo.update_instance(session, **payload.model_dump())
    return ooo

# --- Delete OOO (soft delete) ---
@router.delete(
    "/ooo/{id}",
)
def delete_ooo(
    id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    require_roles(token, [RoleChoices.HR])
    ooo: Optional[DBOOO] = session.query(
        DBOOO
    ).filter_by(
        id=id
    ).first()
    if not ooo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OOO not found")
    ooo.delete_instance(session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

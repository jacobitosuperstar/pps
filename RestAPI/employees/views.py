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

    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if (emp.password != payload.password) or (emp.role == RoleChoices.PRODUCTION.value):
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
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedEmployees:
    require_roles(token, [RoleChoices.HR, RoleChoices.MANAGEMENT])
    
    query = session.query(DBEmployee).filter(DBEmployee.deleted == False)
    
    # Exact match for ID
    if identification:
        query = query.filter(DBEmployee.identification == identification)
    
    # Case-insensitive contains for text fields
    if names:
        query = query.filter(DBEmployee.names.ilike(f"%{names}%"))
    if last_names:
        query = query.filter(DBEmployee.last_names.ilike(f"%{last_names}%"))
    
    # Exact match for enum and boolean
    if role:
        query = query.filter(DBEmployee.role == role)
    if birthday:
        query = query.filter(DBEmployee.birthday == birthday)
    
    # Date range filtering
    if created_at_from:
        query = query.filter(DBEmployee.created_at >= created_at_from)
    if created_at_to:
        query = query.filter(DBEmployee.created_at <= created_at_to)
    if updated_at_from:
        query = query.filter(DBEmployee.updated_at >= updated_at_from)
    if updated_at_to:
        query = query.filter(DBEmployee.updated_at <= updated_at_to)
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply pagination
    results = query.offset(offset).limit(limit).all()
    
    # Convert to response models
    results: List[EmployeeRead] = [
        EmployeeRead.model_validate(emp)
        for emp in results
    ]
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
    try:
        emp: DBEmployee = DBEmployee.create_object(
            session,
            date_joined=date.today(),
            last_login=datetime.now(UTC),
            **payload.model_dump(),
        )
        return emp
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating employee: {str(e)}"
        )


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

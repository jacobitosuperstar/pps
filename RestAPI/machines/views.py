from typing import List, Dict, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session, selectinload
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime, date

from database import get_session
from jwt_authentication.decorators import get_current_user
from employees.models import RoleChoices
from employees.utils import require_roles
from .models import (
    DBMachine,
    Machine,
    MachineRead,
    MachineUpdate,
    PaginatedMachines,
    DBMachineOperator,
    MachineOperator,
    MachineOperatorRead,
    MachineOperatorUpdate,
    PaginatedMachineOperators,
    MachineStatus,
    OperatorSkillLevel,
    DBMachineMaintenance,
    MachineMaintenance,
    MachineMaintenanceRead,
    MachineMaintenanceUpdate,
    PaginatedMachineMaintenance,
    MaintenanceType,
    MaintenanceStatus,
)
from employees.models import DBOOO, OOOTypes


router: APIRouter = APIRouter(
    prefix="/machines",
    tags=["machines"],
)


# ============================================================================
# MACHINE CRUD ENDPOINTS
# ============================================================================

@router.get("/", response_model=PaginatedMachines)
def get_machines(
    machine_id: Optional[int] = None,
    machine_code: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[MachineStatus] = None,
    location: Optional[str] = None,
    manufacturer: Optional[str] = None,
    model: Optional[str] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedMachines:
    """Retrieve machines with flexible filtering and pagination."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    # Build query with flexible filtering
    query = session.query(DBMachine)

    # Exact match for ID and code
    if machine_id:
        query = query.filter(DBMachine.id == machine_id)
    if machine_code:
        query = query.filter(DBMachine.machine_code == machine_code)

    # Case-insensitive contains for text fields
    if name:
        query = query.filter(DBMachine.name.ilike(f"%{name}%"))
    if location:
        query = query.filter(DBMachine.location.ilike(f"%{location}%"))
    if manufacturer:
        query = query.filter(DBMachine.manufacturer.ilike(f"%{manufacturer}%"))
    if model:
        query = query.filter(DBMachine.model.ilike(f"%{model}%"))

    # Exact match for enums
    if status:
        query = query.filter(DBMachine.status == status)

    # Date range filtering
    if created_at_from:
        query = query.filter(DBMachine.created_at >= created_at_from)
    if created_at_to:
        query = query.filter(DBMachine.created_at <= created_at_to)
    if updated_at_from:
        query = query.filter(DBMachine.updated_at >= updated_at_from)
    if updated_at_to:
        query = query.filter(DBMachine.updated_at <= updated_at_to)

    # Boolean filter
    query = query.filter(DBMachine.deleted == deleted)

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination
    results = query.offset(offset).limit(limit).all()

    # Convert to response models
    results: List[MachineRead] = [
        MachineRead.model_validate(m)
        for m in results
    ]
    return PaginatedMachines(results=results, total_count=total_count)


@router.post("/", response_model=MachineRead, status_code=status.HTTP_201_CREATED)
def create_machine(
    payload: Machine,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachine:
    """Create a new machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    # Check if machine code already exists
    existing_machine = session.query(DBMachine).filter_by(machine_code=payload.machine_code).first()
    if existing_machine:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Machine with this code already exists",
        )

    machine: DBMachine = DBMachine.create_object(session=session, **payload.model_dump())
    return machine


@router.get("/{machine_id}", response_model=MachineRead)
def get_machine(
    machine_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachine:
    """Get a machine by ID with its operators and maintenance records."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    machine: Optional[DBMachine] = (
        session.query(DBMachine)
        .options(selectinload(DBMachine.operators), selectinload(DBMachine.maintenance_records))
        .filter_by(id=machine_id)
        .first()
    )

    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    return machine


@router.put("/{machine_id}", response_model=MachineRead)
def update_machine(
    machine_id: int,
    payload: MachineUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachine:
    """Update a machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    machine: Optional[DBMachine] = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    # Check if machine code is being updated and conflicts with existing
    if payload.machine_code and payload.machine_code != machine.machine_code:
        existing_machine = session.query(DBMachine).filter_by(machine_code=payload.machine_code).first()
        if existing_machine:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Machine with this code already exists",
            )

    machine.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return machine


@router.delete("/{machine_id}")
def delete_machine(
    machine_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    machine: Optional[DBMachine] = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    machine.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============================================================================
# MACHINE MAINTENANCE ENDPOINTS
# ============================================================================

@router.get("/{machine_id}/maintenance", response_model=PaginatedMachineMaintenance)
def get_machine_maintenance(
    machine_id: int,
    maintenance_type: Optional[MaintenanceType] = None,
    status: Optional[MaintenanceStatus] = None,
    scheduled_date_from: Optional[str] = None,
    scheduled_date_to: Optional[str] = None,
    actual_date_from: Optional[str] = None,
    actual_date_to: Optional[str] = None,
    deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedMachineMaintenance:
    """Get maintenance records for a specific machine with filtering."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    # Verify machine exists
    machine = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    # Build query
    query = session.query(DBMachineMaintenance).filter_by(machine_id=machine_id)

    if maintenance_type:
        query = query.filter(DBMachineMaintenance.maintenance_type == maintenance_type)
    if status:
        query = query.filter(DBMachineMaintenance.status == status)

    # Date range filtering
    if scheduled_date_from:
        query = query.filter(DBMachineMaintenance.scheduled_date >= scheduled_date_from)
    if scheduled_date_to:
        query = query.filter(DBMachineMaintenance.scheduled_date <= scheduled_date_to)
    if actual_date_from:
        query = query.filter(DBMachineMaintenance.actual_date >= actual_date_from)
    if actual_date_to:
        query = query.filter(DBMachineMaintenance.actual_date <= actual_date_to)

    query = query.filter(DBMachineMaintenance.deleted == deleted)

    total_count = query.count()
    results = query.offset(offset).limit(limit).all()

    results: List[MachineMaintenanceRead] = [
        MachineMaintenanceRead.model_validate(m)
        for m in results
    ]
    return PaginatedMachineMaintenance(results=results, total_count=total_count)


@router.post("/{machine_id}/maintenance", response_model=MachineMaintenanceRead, status_code=status.HTTP_201_CREATED)
def create_machine_maintenance(
    machine_id: int,
    payload: MachineMaintenance,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachineMaintenance:
    """Create a new maintenance record for a machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    # Verify machine exists
    machine = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    maintenance: DBMachineMaintenance = DBMachineMaintenance.create_object(
        session=session,
        machine_id=machine_id,
        **payload.model_dump(exclude={'machine_id'})
    )
    return maintenance


@router.get("/{machine_id}/maintenance/{maintenance_id}", response_model=MachineMaintenanceRead)
def get_maintenance_record(
    machine_id: int,
    maintenance_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachineMaintenance:
    """Get a specific maintenance record."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    maintenance: Optional[DBMachineMaintenance] = session.query(DBMachineMaintenance).filter_by(
        id=maintenance_id,
        machine_id=machine_id
    ).first()

    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found",
        )

    return maintenance


@router.put("/{machine_id}/maintenance/{maintenance_id}", response_model=MachineMaintenanceRead)
def update_maintenance_record(
    machine_id: int,
    maintenance_id: int,
    payload: MachineMaintenanceUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachineMaintenance:
    """Update a maintenance record."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    maintenance: Optional[DBMachineMaintenance] = session.query(DBMachineMaintenance).filter_by(
        id=maintenance_id,
        machine_id=machine_id
    ).first()

    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found",
        )

    maintenance.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return maintenance


@router.delete("/{machine_id}/maintenance/{maintenance_id}")
def delete_maintenance_record(
    machine_id: int,
    maintenance_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a maintenance record."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    maintenance: Optional[DBMachineMaintenance] = session.query(DBMachineMaintenance).filter_by(
        id=maintenance_id,
        machine_id=machine_id
    ).first()

    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found",
        )

    maintenance.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============================================================================
# MACHINE OPERATOR MANAGEMENT ENDPOINTS
# ============================================================================

@router.get("/{machine_id}/operators", response_model=PaginatedMachineOperators)
def get_machine_operators(
    machine_id: int,
    employee_id: Optional[str] = None,
    skill_level: Optional[OperatorSkillLevel] = None,
    deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedMachineOperators:
    """Get operators for a specific machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    # Verify machine exists
    machine = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    # Build query
    query = session.query(DBMachineOperator).filter_by(machine_id=machine_id)

    if employee_id:
        query = query.filter(DBMachineOperator.employee_id == employee_id)
    if skill_level:
        query = query.filter(DBMachineOperator.skill_level == skill_level)

    query = query.filter(DBMachineOperator.deleted == deleted)

    total_count = query.count()
    results = query.offset(offset).limit(limit).all()

    results: List[MachineOperatorRead] = [
        MachineOperatorRead.model_validate(op)
        for op in results
    ]
    return PaginatedMachineOperators(results=results, total_count=total_count)


@router.post("/{machine_id}/operators", response_model=MachineOperatorRead, status_code=status.HTTP_201_CREATED)
def add_machine_operator(
    machine_id: int,
    payload: MachineOperator,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachineOperator:
    """Add an operator to a machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    # Verify machine exists
    machine = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    # Verify employee exists
    from employees.models import DBEmployee
    employee = session.query(DBEmployee).filter_by(identification=payload.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    # Check if operator already exists for this machine
    existing_operator = session.query(DBMachineOperator).filter_by(
        machine_id=machine_id,
        employee_id=payload.employee_id
    ).first()

    if existing_operator:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operator already assigned to this machine",
        )

    operator: DBMachineOperator = DBMachineOperator.create_object(
        session=session,
        machine_id=machine_id,
        **payload.model_dump(exclude={'machine_id'})
    )
    return operator


@router.put("/{machine_id}/operators/{operator_id}", response_model=MachineOperatorRead)
def update_machine_operator(
    machine_id: int,
    operator_id: int,
    payload: MachineOperatorUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBMachineOperator:
    """Update an operator's information for a machine."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    operator: Optional[DBMachineOperator] = session.query(DBMachineOperator).filter_by(
        id=operator_id,
        machine_id=machine_id
    ).first()

    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine operator not found",
        )

    operator.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return operator


@router.delete("/{machine_id}/operators/{operator_id}")
def remove_machine_operator(
    machine_id: int,
    operator_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Remove an operator from a machine (soft delete)."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    operator: Optional[DBMachineOperator] = session.query(DBMachineOperator).filter_by(
        id=operator_id,
        machine_id=machine_id
    ).first()

    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine operator not found",
        )

    operator.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============================================================================
# AVAILABLE OPERATORS ENDPOINT
# ============================================================================

@router.get("/{machine_id}/available-operators")
def get_available_operators(
    machine_id: int,
    date: Optional[date] = None,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[Dict]:
    """Get available operators for a machine considering OOO status."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    # Verify machine exists
    machine = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    # Use current date if not specified
    if not date:
        date = datetime.now().date()

    # Get all operators for this machine
    operators = session.query(DBMachineOperator).filter_by(
        machine_id=machine_id,
        deleted=False
    ).all()

    available_operators = []

    for operator in operators:
        # Get employee information
        from employees.models import DBEmployee
        employee = session.query(DBEmployee).filter_by(
            identification=operator.employee_id
        ).first()

        if not employee:
            continue

        # Check if employee is on OOO
        ooo = session.query(DBOOO).filter(
            DBOOO.employee_id == operator.employee_id,
            DBOOO.deleted == False,
            DBOOO.start_date <= datetime.combine(date, datetime.min.time()),
            DBOOO.end_date >= datetime.combine(date, datetime.min.time())
        ).first()

        is_available = ooo is None

        available_operators.append({
            "employee_id": operator.employee_id,
            "employee_name": f"{employee.names} {employee.last_names}",
            "employee_role": employee.role,
            "skill_level": operator.skill_level,
            "is_available": is_available,
            "ooo_reason": ooo.ooo_type if ooo else None,
            "ooo_end_date": ooo.end_date if ooo else None
        })

    return available_operators

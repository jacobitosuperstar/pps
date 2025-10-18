from typing import List, Optional
from datetime import datetime, UTC
from fastapi.responses import Response
from sqlalchemy.orm import Session, selectinload
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session
from jwt_authentication.decorators import get_current_user
from employees.models import RoleChoices
from employees.utils import require_roles
from .models import (
    DBShift,
    Shift,
    ShiftRead,
    ShiftUpdate,
    PaginatedShifts,
    ShiftType,
    ShiftStatus,
)
from machines.models import DBMachine
from employees.models import DBEmployee
from production.models import DBProductionOrder
from products.models import DBProduct


router: APIRouter = APIRouter(
    prefix="/shifts",
    tags=["shifts"],
)


# ============================================================================
# SHIFT ENDPOINTS
# ============================================================================

@router.get("/", response_model=PaginatedShifts)
def get_shifts(
    shift_id: Optional[int] = None,
    machine_id: Optional[int] = None,
    employee_id: Optional[str] = None,
    production_order_id: Optional[int] = None,
    product_id: Optional[int] = None,
    shift_type: Optional[ShiftType] = None,
    status: Optional[ShiftStatus] = None,
    start_datetime_from: Optional[str] = None,
    start_datetime_to: Optional[str] = None,
    end_datetime_from: Optional[str] = None,
    end_datetime_to: Optional[str] = None,
    deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> PaginatedShifts:
    """Retrieve shifts with flexible filtering and pagination."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION,
            RoleChoices.HR
        ],
    )

    query = session.query(DBShift)

    # Exact match filters
    if shift_id:
        query = query.filter(DBShift.id == shift_id)
    if machine_id:
        query = query.filter(DBShift.machine_id == machine_id)
    if employee_id:
        query = query.filter(DBShift.employee_id == employee_id)
    if production_order_id:
        query = query.filter(DBShift.production_order_id == production_order_id)
    if product_id:
        query = query.filter(DBShift.product_id == product_id)
    if shift_type:
        query = query.filter(DBShift.shift_type == shift_type)
    if status:
        query = query.filter(DBShift.status == status)

    # Datetime range filters
    if start_datetime_from:
        query = query.filter(DBShift.start_datetime >= start_datetime_from)
    if start_datetime_to:
        query = query.filter(DBShift.start_datetime <= start_datetime_to)
    if end_datetime_from:
        query = query.filter(DBShift.end_datetime >= end_datetime_from)
    if end_datetime_to:
        query = query.filter(DBShift.end_datetime <= end_datetime_to)

    # Boolean filter
    query = query.filter(DBShift.deleted == deleted)

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination and load relationships
    results = (
        query.options(
            selectinload(DBShift.machine),
            selectinload(DBShift.employee),
            selectinload(DBShift.production_order),
            selectinload(DBShift.product)
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Convert to response models
    results = [ShiftRead.model_validate(s) for s in results]
    return PaginatedShifts(results=results, total_count=total_count)


@router.post("/", response_model=ShiftRead, status_code=status.HTTP_201_CREATED)
def create_shift(
    payload: Shift,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBShift:
    """Create a new shift."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    try:
        # Validate machine exists
        machine = session.query(DBMachine).filter_by(id=payload.machine_id).first()
        if not machine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Machine not found",
            )

        # Validate employee exists
        employee = session.query(DBEmployee).filter_by(identification=payload.employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )

        # Validate production order exists (if provided)
        if payload.production_order_id:
            production_order = session.query(DBProductionOrder).filter_by(id=payload.production_order_id).first()
            if not production_order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Production order not found",
                )

        # Validate product exists (if provided)
        if payload.product_id:
            product = session.query(DBProduct).filter_by(id=payload.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found",
                )

        # Validate that production shifts have a product
        if payload.shift_type == ShiftType.PRODUCTION and not payload.product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product ID is required for production shifts",
            )

        # Validate datetime logic
        if payload.start_datetime >= payload.end_datetime:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start datetime must be before end datetime",
            )

        # Generate production code for production shifts
        production_code = None
        if payload.shift_type == ShiftType.PRODUCTION and payload.product_id:
            # Get machine code and product name for production code generation
            machine_code = machine.machine_code
            product_name = product.name

            # Generate unique production code: MACHINE_CODE-PRODUCT_NAME-TIMESTAMP
            timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
            production_code = f"{machine_code}-{product_name[:10].upper()}-{timestamp}"

            # Ensure uniqueness
            existing_code = session.query(DBShift).filter_by(production_code=production_code).first()
            counter = 1
            original_code = production_code
            while existing_code:
                production_code = f"{original_code}-{counter:02d}"
                existing_code = session.query(DBShift).filter_by(production_code=production_code).first()
                counter += 1

        # Create shift with generated production code
        start_dt = payload.start_datetime
        end_dt = payload.end_datetime

        # Use create_object method now that Base model is fixed
        db_shift = DBShift.create_object(
            session=session,
            machine_id=payload.machine_id,
            employee_id=payload.employee_id,
            production_order_id=payload.production_order_id,
            product_id=payload.product_id,
            shift_type=payload.shift_type.value,
            status=payload.status.value,
            start_datetime=start_dt,
            end_datetime=end_dt,
            production_code=production_code,
            description=payload.description,
            notes=payload.notes
        )

        return db_shift
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating shift: {str(e)}"
        )


# ============================================================================
# SPECIALIZED ENDPOINTS (must be before /{shift_id})
# ============================================================================


@router.get("/machine/{machine_id}/shifts", response_model=List[ShiftRead])
def get_machine_shifts(
    machine_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    shift_type: Optional[ShiftType] = None,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[ShiftRead]:
    """Get all shifts for a specific machine within a date range."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION
        ],
    )

    # Validate machine exists
    machine = session.query(DBMachine).filter_by(id=machine_id).first()
    if not machine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Machine not found",
        )

    query = (
        session.query(DBShift)
        .options(
            selectinload(DBShift.machine),
            selectinload(DBShift.employee),
            selectinload(DBShift.production_order),
            selectinload(DBShift.product)
        )
        .filter_by(machine_id=machine_id, deleted=False)
    )

    # Apply date filters if provided
    if date_from:
        query = query.filter(DBShift.start_datetime >= date_from)
    if date_to:
        query = query.filter(DBShift.end_datetime <= date_to)

    # Apply shift type filter if provided
    if shift_type:
        query = query.filter(DBShift.shift_type == shift_type)

    shifts = query.order_by(DBShift.start_datetime).all()
    return [ShiftRead.model_validate(s) for s in shifts]


@router.get("/employee/{employee_id}/shifts", response_model=List[ShiftRead])
def get_employee_shifts(
    employee_id: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[ShiftRead]:
    """Get all shifts for a specific employee within a date range."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.HR
        ],
    )

    # Validate employee exists
    employee = session.query(DBEmployee).filter_by(identification=employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    query = (
        session.query(DBShift)
        .options(
            selectinload(DBShift.machine),
            selectinload(DBShift.employee),
            selectinload(DBShift.production_order),
            selectinload(DBShift.product)
        )
        .filter_by(employee_id=employee_id, deleted=False)
    )

    # Apply date filters if provided
    if date_from:
        query = query.filter(DBShift.start_datetime >= date_from)
    if date_to:
        query = query.filter(DBShift.end_datetime <= date_to)

    shifts = query.order_by(DBShift.start_datetime).all()
    return [ShiftRead.model_validate(s) for s in shifts]


@router.get("/{shift_id}", response_model=ShiftRead)
def get_shift(
    shift_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBShift:
    """Get a shift by ID."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER,
            RoleChoices.PRODUCTION,
            RoleChoices.HR
        ],
    )

    shift = (
        session.query(DBShift)
        .options(
            selectinload(DBShift.machine),
            selectinload(DBShift.employee),
            selectinload(DBShift.production_order),
            selectinload(DBShift.product)
        )
        .filter_by(id=shift_id)
        .first()
    )

    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    return shift


@router.put("/{shift_id}", response_model=ShiftRead)
def update_shift(
    shift_id: int,
    payload: ShiftUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DBShift:
    """Update a shift."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    shift = session.query(DBShift).filter_by(id=shift_id).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    # Validate production order exists (if provided)
    if payload.production_order_id:
        production_order = session.query(DBProductionOrder).filter_by(id=payload.production_order_id).first()
        if not production_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Production order not found",
            )

    # Validate product exists (if provided)
    if payload.product_id:
        product = session.query(DBProduct).filter_by(id=payload.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

    # Validate datetime logic (if datetimes are being updated)
    if payload.start_datetime and payload.end_datetime:
        if payload.start_datetime >= payload.end_datetime:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start datetime must be before end datetime",
            )
    elif payload.start_datetime and not payload.end_datetime:
        if payload.start_datetime >= shift.end_datetime:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Start datetime must be before current end datetime",
            )
    elif payload.end_datetime and not payload.start_datetime:
        if shift.start_datetime >= payload.end_datetime:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End datetime must be after current start datetime",
            )

    shift.update_instance(session=session, **payload.model_dump(exclude_unset=True))
    return shift


@router.delete("/{shift_id}")
def delete_shift(
    shift_id: int,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Response:
    """Soft delete a shift."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.PRODUCTION_MANAGER
        ],
    )

    shift = session.query(DBShift).filter_by(id=shift_id).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    shift.delete_instance(session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from typing import List, Dict, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session

from jwt_authentication.decorators import get_current_user
from employees.models import (
    RoleChoices,
)
from employees.utils import require_roles

from .models import (
    DBClient,
    Client,
    ClientRead,
    ClientUpdate,
    PaginatedClients,
)


router: APIRouter = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.get(path="/", response_model=PaginatedClients)
def get_clients(
    client_id: Optional[str] = None,
    client_name: Optional[str] = None,
    client_email: Optional[str] = None,
    client_phone_code: Optional[str] = None,
    client_phone_number: Optional[str] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    updated_at_from: Optional[str] = None,
    updated_at_to: Optional[str] = None,
    client_deleted: bool = False,
    token=Depends(get_current_user),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
) -> PaginatedClients:
    """Retrieve clients with flexible filtering and pagination.

    Filtering options:
    - client_id: Exact match
    - client_name: Case-insensitive contains search
    - client_email: Case-insensitive contains search
    - client_phone_code: Case-insensitive contains search
    - client_phone_number: Case-insensitive contains search
    - created_at_from/created_at_to: Date range filtering
    - updated_at_from/updated_at_to: Date range filtering
    - client_deleted: Boolean filter
    """
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING
        ],
    )

    # Build query with flexible filtering
    query = session.query(DBClient)

    # Exact match for ID
    if client_id:
        query = query.filter(DBClient.client_id == client_id)

    # Case-insensitive contains for text fields
    if client_name:
        query = query.filter(DBClient.client_name.ilike(f"%{client_name}%"))
    if client_email:
        query = query.filter(DBClient.client_email.ilike(f"%{client_email}%"))
    if client_phone_code:
        query = query.filter(DBClient.client_phone_code.ilike(f"%{client_phone_code}%"))
    if client_phone_number:
        query = query.filter(DBClient.client_phone_number.ilike(f"%{client_phone_number}%"))

    # Date range filtering
    if created_at_from:
        query = query.filter(DBClient.created_at >= created_at_from)
    if created_at_to:
        query = query.filter(DBClient.created_at <= created_at_to)
    if updated_at_from:
        query = query.filter(DBClient.updated_at >= updated_at_from)
    if updated_at_to:
        query = query.filter(DBClient.updated_at <= updated_at_to)

    # Boolean filter
    query = query.filter(DBClient.deleted == client_deleted)

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination
    results = query.offset(offset).limit(limit).all()

    # Convert to response models
    results: List[ClientRead] = [
        ClientRead.model_validate(c)
        for c in results
    ]
    return PaginatedClients(results=results, total_count=total_count)


@router.post(
    "/",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED
)
def create_client(
    payload: Client,
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
    response_model=ClientRead,
) -> DBClient:
    """Create a new active client."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING
        ],
    )
    client: Optional[DBClient] = session.query(DBClient).filter_by(client_id=payload.client_id).first()
    if client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client already exists",
        )
    db_client: DBClient = DBClient.create_object(session=session, **payload.model_dump())
    return db_client


@router.get("/{client_id}", response_model=ClientRead)
def get_client(
    client_id: str,
    token=Depends(get_current_user),
    session: Session = Depends(dependency=get_session),
) -> DBClient:
    """Get a client."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING
        ],
    )
    client: Optional[DBClient] = session.query(DBClient).filter_by(client_id=client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client doesn't exists.",
        )
    return client


@router.post("/{client_id}")
def update_client(
    client_id: str,
    payload: ClientUpdate,
    token=Depends(get_current_user),
    session: Session = Depends(dependency=get_session),
    response_model=ClientRead,
) -> Client:
    """Update an active client."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING
        ],
    )
    client: Optional[DBClient] = session.query(DBClient).filter_by(client_id=client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client doesn't exists.",
        )
    client.update_instance(session=session, **payload.model_dump())
    return client


@router.delete("/{client_id}")
def delete_client(
    client_id: str,
    token=Depends(get_current_user),
    session: Session = Depends(dependency=get_session),
) -> Response:
    """Update an active client."""
    require_roles(
        token=token,
        allowed_roles=[
            RoleChoices.MANAGEMENT,
            RoleChoices.ACCOUNTING
        ],
    )
    client: Optional[DBClient] = session.query(DBClient).filter_by(client_id=client_id).first()
    if client:
        client.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

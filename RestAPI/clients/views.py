from typing import List, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query

from database import get_session
from .models import (
    DBClient,
    Client,
    ClientRead,
    ClientUpdate,
    PaginatedClients,
)
from base.db_base_services import filter_instances


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
    client_deleted: bool = False,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """
    Retrieve clients (optionally including deleted ones), with optional filtering by fields and pagination.
    Use the client_deleted query parameter to include deleted clients if needed.
    """
    filters = {
        "deleted": client_deleted,
        "client_id": client_id,
        "client_name": client_name,
        "client_email": client_email,
        "client_phone_code": client_phone_code,
        "client_phone_number": client_phone_number,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    clients, total_count = filter_instances(DBClient, session, filters, limit=limit, offset=offset)
    # Use Pydantic model for serialization
    results = [ClientRead.model_validate(c) for c in clients]
    return PaginatedClients(results=results, total_count=total_count)


@router.post("/", response_model=ClientRead)
def create_client(
    payload: Client,
    session: Session = Depends(get_session),
) -> DBClient:
    """Create a new active client."""
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
    session: Session = Depends(dependency=get_session),
) -> DBClient:
    """Get a client."""
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
    session: Session = Depends(dependency=get_session),
) -> Client:
    """Update an active client."""
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
    session: Session = Depends(dependency=get_session),
) -> Response:
    """Update an active client."""
    client: Optional[DBClient] = session.query(DBClient).filter_by(client_id=client_id).first()
    if client:
        client.delete_instance(session=session, soft_delete=True)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

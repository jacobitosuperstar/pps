from typing import List, Optional
from fastapi.responses import Response
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from database import get_session
from .models import (
    DBClient,
    Client,
    ClientRead,
    ClientUpdate,
)


router: APIRouter = APIRouter(
    prefix="/clients",
    tags=["clients"],
)



@router.get(path="/", response_model=List[ClientRead])
def get_clients(
    session: Session = Depends(get_session),
) -> List[DBClient]:
    """
    Retrieve all active clients (not soft-deleted).
    - Query the database filtering where `deleted == False`.
    - Return a list of Pydantic ClientRead models.
    """
    clients: List[DBClient] = session.query(DBClient).filter_by(deleted=False).all()
    return clients


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

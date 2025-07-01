from typing import Optional, List
from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from base.models import Base, PaginatedElements



class DBClient(Base):
    """
    Clients to which the company generates production orders.

    Attributes:
        client_id: Unique identifier for the client (CC/NIT).
        client_name: Name of the client.
        client_email: Email of the client.
        client_phone_code: Country code (e.g., "+57").
        client_phone_number: Client's phone number.
        created_at: When the record was created.
        updated_at: When the record was last updated.
        deleted: Soft delete flag.
    """
    __tablename__ = "client"

    client_id = Column(
        String,
        primary_key=True,
        nullable=False,
        index=True,
    )
    client_name = Column(
        String(100),
        nullable=False,
    )
    client_email = Column(
        String(100),
        nullable=False,
    )
    client_phone_code = Column(
        String(10),
        nullable=False,
        default="+57",
    )
    client_phone_number = Column(
        String(20),
        nullable=False,
    )

    # Relationships
    sale_orders = relationship("DBSaleOrder", back_populates="client")



class Client(BaseModel):
    client_id: str = Field(
        ...,
        description="Unique identifier for the client (CC/NIT)",
    )
    client_name: str = Field(
        ...,
        max_length=100,
    )
    client_email: EmailStr
    client_phone_code: Optional[str] = Field(
        "+57",
        max_length=10,
    )
    client_phone_number: str = Field(
        ...,
        max_length=25
    )


class ClientUpdate(BaseModel):
    client_name: Optional[str] = Field(
        None,
        max_length=100,
    )
    client_email: Optional[EmailStr] = None
    client_phone_code: Optional[str] = Field(
        None,
        max_length=10,
    )
    client_phone_number: Optional[str] = Field(
        None,
        max_length=20,
    )


class ClientRead(Client):
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = ConfigDict(from_attributes=True)


# Type alias for paginated clients
PaginatedClients = PaginatedElements[ClientRead]
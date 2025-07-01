from typing import Type, TypeVar, List, Generic
from typing_extensions import TypedDict
from datetime import datetime, UTC
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
)

from database import DeclarativeBase


T = TypeVar("T", bound="Base")
PydanticT = TypeVar("PydanticT", bound=BaseModel)


class TestResponse(TypedDict):
    now: datetime


class PaginatedElements(BaseModel, Generic[PydanticT]):
    """
    Generic paginated response model that can work with any Pydantic model.
    
    Args:
        results: List of items of type PydanticT
        total_count: Total number of items (before pagination)
    """
    results: List[PydanticT]
    total_count: int


class Base(DeclarativeBase):
    __abstract__: bool = True

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    @classmethod
    def create_object(cls: Type[T], session: Session, **kwargs) -> T:
        """Creates a new instance of the model into the database."""
        instance = cls(**kwargs)
        session.add(instance=instance)
        session.commit()
        session.refresh(instance=instance)
        return instance

    def update_instance(self, session: Session, **kwargs) -> None:
        """Updates the current instance of the model."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.now(UTC)
        session.add(self)
        session.commit()
        session.refresh(self)

    def delete_instance(self, session: Session, soft_delete: bool = True) -> None:
        """Soft or hard delete the instance."""
        if soft_delete:
            self.deleted = True
            self.updated_at = datetime.now(UTC)
            session.add(self)
        else:
            session.delete(self)
        session.commit()

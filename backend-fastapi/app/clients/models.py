from sqlalchemy import Column, String, Text
from app.db.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    contact_person = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

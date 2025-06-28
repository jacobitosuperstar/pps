from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.base import Base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Crear una sesión para verificar que todo está bien
with Session(engine) as session:
    # Solo para verificar que la conexión funciona
    session.execute("SELECT 1")
    session.commit()

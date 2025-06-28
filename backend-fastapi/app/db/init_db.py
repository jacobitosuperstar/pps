from app.db import Base, engine, SessionLocal
from app.core.config import settings

# Crear todas las tablas
print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas exitosamente")

# Crear una sesión para verificar que todo está bien
print("Verificando conexión...")
with SessionLocal() as session:
    # Solo para verificar que la conexión funciona
    session.execute("SELECT 1")
    session.commit()
print("Base de datos inicializada correctamente")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="PPS Backend API",
    description="API para el sistema de Producción y Planificación",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de cada módulo
from app.employees import employees_router
from app.machines import machines_router
from app.products import products_router
from app.production import production_router

app.include_router(employees_router, prefix="/api/v1")
app.include_router(machines_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(production_router, prefix="/api/v1")

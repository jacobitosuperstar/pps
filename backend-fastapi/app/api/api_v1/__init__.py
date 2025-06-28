from fastapi import APIRouter

api_router = APIRouter()

from .endpoints.employees import router as employees_router
from .endpoints.machines import router as machines_router
from .endpoints.products import router as products_router
from .endpoints.production import router as production_router

api_router.include_router(employees_router)
api_router.include_router(machines_router)
api_router.include_router(products_router)
api_router.include_router(production_router)

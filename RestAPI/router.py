from fastapi.routing import APIRouter
from base.views import router as base_router
from clients.views import router as clients_router
from employees.views import router as employees_router
from products.views import router as products_router
from production.views import router as production_router
from machines.views import router as machines_router
from shift.views import router as shift_router


api_router: APIRouter = APIRouter()
api_router.include_router(base_router)
api_router.include_router(clients_router)
api_router.include_router(employees_router)
api_router.include_router(products_router)
api_router.include_router(production_router)
api_router.include_router(machines_router)
api_router.include_router(shift_router)

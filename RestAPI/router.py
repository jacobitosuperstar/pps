from fastapi.routing import APIRouter
from base.views import router as base_router
from employees.views import router as employees_router


api_router: APIRouter = APIRouter()
api_router.include_router(base_router)
api_router.include_router(employees_router)

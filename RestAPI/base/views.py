import datetime
from fastapi import APIRouter, Depends

from .models import TestResponse
from jwt_authentication.decorators import get_current_user


router: APIRouter = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
def ping() -> TestResponse:
    """Checking the health of the server.
    """
    return TestResponse(now=datetime.datetime.now())


@router.get("/logged-ping")
def logged_ping(token_payload=Depends(get_current_user)):
    """Ping endpoint that requires authentication. Returns the same TestResponse as ping, but requires authentication."""
    return TestResponse(now=datetime.datetime.now())

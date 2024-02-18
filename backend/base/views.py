from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import now

from jwt_authentication.decorators import authenticated_user


@require_GET
def pin_view(request: HttpRequest) -> HttpResponse:
    """Server pining. To check that the server is alive and getting the csrf
    cookie.

    Parameters
    ----------
    request: HttpRequest
        - GET

    Returns
    -------
    JsonResponse
        Json Object with the current time.
    """
    return HttpResponse(b"")


@require_GET
@authenticated_user
def logged_pin_view(request: HttpRequest) -> JsonResponse:
    """Server pining. To check that the server is alive and getting the csrf
    cookie.

    Parameters
    ----------
    request: HttpRequest
        - GET

    Returns
    -------
    JsonResponse
        Json Object with the current time.
    """
    msg = {"now": now()}
    response = JsonResponse(msg)
    return response

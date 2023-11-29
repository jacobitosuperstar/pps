from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now



@require_GET
def new_pin_view(request: HttpRequest) -> HttpResponse:
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
@ensure_csrf_cookie
def pin_view(request: HttpRequest) -> JsonResponse:
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


@require_GET
@login_required
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

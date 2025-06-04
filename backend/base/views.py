from django.http import (
    HttpRequest,
)
from django.views.decorators.http import require_GET
from django.utils.timezone import now
from django.views import View
from django.http import HttpResponse, Http404

import os

from jwt_authentication.decorators import authenticated_user
from .response import ORJsonResponse as JsonResponse


@require_GET
def pin_view(_: HttpRequest) -> JsonResponse:
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
@authenticated_user
def logged_pin_view(_: HttpRequest) -> JsonResponse:
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

class ReactAppView(View):
    def get(self, request, *args, **kwargs):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            raise Http404("React build not found")
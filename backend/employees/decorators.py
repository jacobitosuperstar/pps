from typing import Callable, Union, Optional, List
from functools import wraps, partial

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext as _
from jwt_authentication.jwt_authentication import decode_token
from base.http_status_codes import HTTP_STATUS as http
from rest_framework.permissions import BasePermission


def role_validation(
    allowed_roles: List[str],
    view: Optional[Callable] = None,
) -> Callable:
    """Given a view, evaluates the role of the user. If the role matches with
    the one required by the view, the procedure continues, else a JsonResponse
    is returned.
    """

    if view is None:
        return partial(role_validation, allowed_roles)

    @wraps(view)
    def wrapper(
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> Union[Callable, JsonResponse]:
        # getting token from the request
        # This is done again because we are having issues with object
        # consistency in the request object modification.
        auth_header = request.META['HTTP_AUTHORIZATION']
        token = auth_header.split(' ')[1]
        try:
            token_payload = decode_token(token)
        except InvalidSignatureError as e:
            message = {"response": e}
            return JsonResponse(message, status=http.forbidden)
        except ExpiredSignatureError as e:
            message = {"response": e}
            return JsonResponse(message, status=http.forbidden)
        # checking the role
        if token_payload.get("employee_role") not in allowed_roles:
            msg = {"response": _("Role not allowed to do this operation")}
            response = JsonResponse(msg, status=http.forbidden)
            return response
        return view(request, *args, **kwargs)
    return wrapper

class IsEmployeeInRole(BasePermission):
    """
    Permite el acceso solo a empleados cuyo rol esté en la lista permitida.
    """

    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []

    def has_permission(self, request, view):
        user = request.user
        # Verificar que el usuario esté autenticado y tenga atributo `role`
        if not user or not user.is_authenticated:
            return False
        
        return user.role in self.allowed_roles
    
def IsEmployeeRole(allowed_roles):
    class Permission(IsEmployeeInRole):
        def __init__(self):
            super().__init__(allowed_roles=allowed_roles)
    return Permission

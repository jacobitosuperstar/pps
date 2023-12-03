from typing import Callable, Union, Optional, List
from functools import wraps, partial
from django.http import HttpRequest, JsonResponse
from .models import Employee
from base.http_status_codes import HTTP_STATUS as status


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
        # getting the user from the request
        token_payload = request.token_payload
        # checking the role
        if token_payload.get("employee_role") not in allowed_roles:
            msg = {"response": "Role not allowed to do this operation"}
            response = JsonResponse(msg, status=status.forbidden)
            return response
        return view(request, *args, **kwargs)
    return wrapper

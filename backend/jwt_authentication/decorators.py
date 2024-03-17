from typing import Callable, Union, Optional
from functools import wraps, partial

from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

from django.http import HttpRequest, JsonResponse

from base.http_status_codes import HTTP_STATUS as http
from jwt_authentication.jwt_authentication import decode_token


def authenticated_user(
    view: Optional[Callable] = None,
) -> Callable:
    """Checks if the JWT passed is valid and puts the payload in the
    "token_payload" parameter of the request object.
    """
    if view is None:
        return partial(authenticated_user)

    @wraps(view)
    def wrapper(
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> Union[Callable, JsonResponse]:
        # getting the user from the request
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Token '):
            token = auth_header.split(' ')[1]
            try:
                token_payload = decode_token(token)
            except InvalidSignatureError as e:
                message = {"response": e}
                return JsonResponse(message, status=http.forbidden)
            except ExpiredSignatureError as e:
                message = {"response": e}
                return JsonResponse(message, status=http.forbidden)
        return view(request, *args, **kwargs)
    return wrapper

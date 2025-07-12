from typing import (
    Any,
    Dict,
)
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)
from datetime import datetime, timedelta

from employees.models import Employee

try:
    from django.utils.translation import gettext as _
    from django.conf import settings


    SECRET_KEY = settings.SECRET_KEY
    if hasattr(settings, "JWT_EXPIRATION_TIME"):
        EXPIRATION = settings.JWT_EXPIRATION_TIME
    else:
        EXPIRATION = 1209600
except ImportError:
    SECRET_KEY = ""
    EXPIRATION = 1209600


def create_token(**kwargs):
    """Creates a JWT with the named arguments passed. Adds the expiration time
    to the payload automaticaly.
    """
    expiration_date = datetime.now() + timedelta(seconds=EXPIRATION)
    expiration = int(expiration_date.timestamp())
    payload = {"exp": expiration}
    payload = {**payload, **kwargs}
    encoded_jwt = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decodes a JWT token and returns it's payload.
    """
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=["HS256"])
        return payload
    except InvalidSignatureError:
        raise InvalidSignatureError(_("Invalid Signature."))
    except ExpiredSignatureError:
        raise ExpiredSignatureError(_("The token has expired."))
    


class JWTAuthentication(BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        # Validar si el encabezado existe y sigue el formato esperado
        if not auth_header or not auth_header.startswith(f"{self.keyword} "):
            return None  # Indica que no se puede autenticar, pero no lanza error aún

        token = auth_header[len(self.keyword) + 1:].strip()

        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise AuthenticationFailed(_("Token has expired."))
        except InvalidSignatureError:
            raise AuthenticationFailed(_("Invalid token signature."))
        except jwt.DecodeError:
            raise AuthenticationFailed(_("Malformed token."))
        except Exception:
            raise AuthenticationFailed(_("Could not decode token."))

        employee_id = payload.get("employee_id")
        if not employee_id:
            raise AuthenticationFailed(_("Invalid payload: missing employee_id."))

        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist: # pylint: disable=no-member
            raise AuthenticationFailed(_("Employee not found."))

        return (employee, token)

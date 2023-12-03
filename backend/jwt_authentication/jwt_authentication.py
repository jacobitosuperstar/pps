from typing import (
    Any,
    Dict,
)
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)
from datetime import datetime, timedelta

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

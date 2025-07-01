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
from settings import settings

SECRET_KEY = settings.secret_key
EXPIRATION = settings.acces_token_experation


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
    """Decodes a JWT token and returns its payload.
    """
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=["HS256"])
        return payload
    except InvalidSignatureError:
        raise InvalidSignatureError("Invalid Signature.")
    except ExpiredSignatureError:
        raise ExpiredSignatureError("The token has expired.")

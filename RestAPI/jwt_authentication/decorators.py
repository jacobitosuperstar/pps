from typing import Dict
from fastapi import Request, HTTPException, status
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
)
from jwt_authentication.jwt_authentication import decode_token

# Synchronous version
def get_current_user(request: Request) -> Dict:
    """
    FastAPI dependency (sync) that checks the JWT in the Authorization header and returns the payload.
    Raises HTTPException if the token is missing, invalid, or expired.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Token "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header."
        )
    token = auth_header.split(" ", 1)[1]
    try:
        token_payload = decode_token(token)
        return token_payload
    except InvalidSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

# Asynchronous version
async def get_current_user_async(request: Request) -> Dict:
    """
    FastAPI dependency (async) that checks the JWT in the Authorization header and returns the payload.
    Raises HTTPException if the token is missing, invalid, or expired.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Token "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header."
        )
    token = auth_header.split(" ", 1)[1]
    try:
        token_payload = decode_token(token)
        return token_payload
    except InvalidSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

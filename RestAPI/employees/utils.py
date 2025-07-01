from fastapi import HTTPException, status
from typing import List, Any

def require_roles(token: dict, allowed_roles: List[Any]):
    """
    Raises HTTPException if the user's role is not in allowed_roles.
    Usage: require_roles(token, [Roles.HR, Roles.MANAGEMENT])
    """
    if token["employee_role"] not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        ) 
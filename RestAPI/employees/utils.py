from fastapi import HTTPException, status
from typing import List, Any
from settings import settings

def require_roles(token: dict, allowed_roles: List[Any]):
    """
    Raises HTTPException if the user's role is not in allowed_roles.
    Usage: require_roles(token, [Roles.HR, Roles.MANAGEMENT])
    
    If DISABLE_AUTH is True, always passes (for testing purposes).
    """
    # Check if authentication is disabled for testing
    if settings.disable_auth:
        return  # Always pass when auth is disabled
    
    if token.get("employee_role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

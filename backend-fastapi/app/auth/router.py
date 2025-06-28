from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from . import services, schemas
from app.employees import models as employee_models

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = services.authenticate_user(
        db, 
        username=form_data.username, 
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = services.create_access_token_for_user(user)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users/me/", response_model=schemas.UserInDB)
async def read_users_me(
    current_user: employee_models.Employee = Depends(services.get_current_active_user)
):
    return current_user

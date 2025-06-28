from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    identification: str
    names: str
    last_names: str
    role: str
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

    class Config:
        from_attributes = True

from pydantic_settings import BaseSettings
from typing import List
from datetime import timedelta

class Settings(BaseSettings):
    PROJECT_NAME: str = "PPS Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    
    # Database
    DATABASE_URL: str = "sqlite:///./pps.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Token configuration
    @property
    def ACCESS_TOKEN_EXPIRE(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    class Config:
        case_sensitive = True

settings = Settings()

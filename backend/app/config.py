"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Coding Teacher"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./coding_teacher.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Code Execution (Piston API - free, no key required)
    PISTON_API_URL: str = "https://emkc.org/api/v2/piston"
    
    # Redis (optional, for caching)
    REDIS_URL: str = "redis://localhost:6379"
    USE_REDIS: bool = False
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


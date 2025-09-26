from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    
    # Database
    DATABASE_URL: str = "sqlite:///./db.sqlite"
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "http://localhost", "*"]
    
    # Server settings
    USE_FORWARDED_HOST: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
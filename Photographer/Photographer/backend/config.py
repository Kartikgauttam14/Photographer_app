from pydantic import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "PhotoHire"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost/photohire"
    
    # Authentication Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    
    # Firebase Settings
    FIREBASE_CREDENTIALS: Optional[str] = None
    
    # File Storage Settings
    UPLOAD_DIRECTORY: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5_242_880  # 5MB
    
    # Socket.IO Settings
    SOCKETIO_CORS_ORIGINS: str = "*"
    
    # Location Settings
    LOCATION_UPDATE_INTERVAL: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Create a settings instance
settings = get_settings()
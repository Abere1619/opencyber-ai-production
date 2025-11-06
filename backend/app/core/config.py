import os
from typing import List, Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpenCyber AI Platform"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    DATABASE_URL: str = "postgresql://opencyber:password@localhost/opencyber_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # ML Configuration
    TENSORFLOW_MODEL_PATH: str = "./ml_models/tensorflow/"
    PYTORCH_MODEL_PATH: str = "./ml_models/pytorch/"
    
    # File Upload
    MAX_FILE_SIZE: int = 100 * 1024 * 1024
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_FILE_TYPES: List[str] = [
        "text/plain", "application/pdf", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/x-msdownload", "application/x-dosexec"
    ]
    
    # Monitoring
    ENABLE_METRICS: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

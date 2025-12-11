
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FINCRAWL"
    API_V1_STR: str = "/api/v1"
    
    # Fallback to SQLite for local hack mode without Docker
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fincrawl.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "") # Empty means no Redis
    
    # Storage
    USE_LOCAL_STORAGE: bool = os.getenv("USE_LOCAL_STORAGE", "true").lower() == "true"
    LOCAL_STORAGE_PATH: str = "local_data"
    
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "fincrawl-raw")
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings()

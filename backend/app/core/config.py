import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FINCRAWL"
    API_V1_STR: str = "/api/v1"
    
    REDIS_URL: str = "" # Empty means no Redis
    
    # Storage
    USE_LOCAL_STORAGE: bool = True
    LOCAL_STORAGE_PATH: str = "local_data"
    PERSISTENT_DATA_PATH: str = "" # For Render Disk

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "fincrawl-raw"
    MINIO_SECURE: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Check for an explicit DATABASE_URL environment variable first
        explicit_db_url = os.getenv("DATABASE_URL")
        if explicit_db_url:
            return explicit_db_url
        
        # Fallback to SQLite, using PERSISTENT_DATA_PATH if available
        if self.PERSISTENT_DATA_PATH:
             return f"sqlite:///{self.PERSISTENT_DATA_PATH}/fincrawl.db"
        return "sqlite:///./fincrawl.db" # Default local SQLite path

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

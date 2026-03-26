from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

# BaseSettings from pydantic takes care of .env vars (no need for os.getenv or similar)
class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "ESL lessons backend"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()




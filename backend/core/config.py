from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Trading Assistant"
    API_V1_STR: str = "/api/v1"
    
    # Auth
    SECRET_KEY: str = "supersecretkey_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    MYSQL_URL: str = "mysql+aiomysql://user:password@localhost:3306/ai_trading"
    
    # Vector DB
    QDRANT_URL: str = "http://localhost:6333"
    
    # LLM
    OPENAI_API_KEY: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application Configuration"""
    
    # App Settings
    APP_NAME: str = "AI Job Hunter"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # API Keys
    FOORILLA_API_KEY: str = os.getenv("FOORILLA_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/job_hunter.db")
    
    # LLM Settings
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Paths
    UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "./resumes/uploads")
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "./logs")
    
    # Foorilla API Settings
    FOORILLA_BASE_URL: str = "https://jobdataapi.com/api"
    FOORILLA_TIMEOUT: int = 30
    
    # Application Settings
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 10
    
    # Resume Settings
    MAX_RESUME_SIZE_MB: int = 5
    SUPPORTED_RESUME_FORMATS: list = ["pdf", "docx"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure directories exist
for directory in [settings.UPLOADS_DIR, settings.DATA_DIR, settings.LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

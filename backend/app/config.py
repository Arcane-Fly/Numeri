import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./numeri.db"
    database_url_async: str = "sqlite+aiosqlite:///./numeri.db"
    
    # Application
    app_name: str = "Numeri - ATO Tax Preparation"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_prefix: str = "/api"
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Document processing
    upload_directory: str = "./uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".pdf", ".png", ".jpg", ".jpeg"]
    
    # OCR settings
    tesseract_cmd: Optional[str] = None  # Will use system default
    
    # Tax year settings
    current_tax_year: str = "2024-25"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"


settings = Settings()
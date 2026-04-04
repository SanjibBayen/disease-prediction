"""
Configuration settings for the application
"""

import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE: str = os.getenv("API_TITLE", "HealthPredict AI API")
    API_VERSION: str = os.getenv("API_VERSION", "3.0.0")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "Advanced Disease Prediction System")
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = eval(os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:5173"]'))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # AI APIs
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
    
    # Model Paths
    MODEL_BASE_PATH: str = os.getenv("MODEL_BASE_PATH", "models")
    
    # Data Paths
    DATA_BASE_PATH: str = os.getenv("DATA_BASE_PATH", "data")

settings = Settings()
"""
MayaStudio AI - Configuration Settings
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "MayaStudio AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    FRONTEND_URL: str = "http://localhost:3000"

    # Database (Supabase PostgreSQL)
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str  # Service role key (backend only)

    # Google Cloud
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GEMINI_API_KEY: str
    GOOGLE_APPLICATION_CREDENTIALS_JSON: Optional[str] = None

    # Google Drive
    GOOGLE_DRIVE_SCOPES: list = [
        "https://www.googleapis.com/auth/drive.file"
    ]

    # File Processing
    TEMP_DIR: str = "/app/temp"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_EXTENSIONS: list = [".mp4", ".mov", ".avi"]
    ALLOWED_AUDIO_EXTENSIONS: list = [".mp3", ".wav", ".m4a"]

    # TTS Settings
    DEFAULT_LANGUAGE_CODE: str = "si-LK"  # Sinhala
    DEFAULT_VOICE_GENDER: str = "NEUTRAL"

    # FFmpeg Settings
    FFMPEG_VIDEO_CODEC: str = "libx264"
    FFMPEG_AUDIO_CODEC: str = "aac"
    FFMPEG_CRF: int = 23  # Quality (lower = better, 18-28 is good range)

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://mayastudio.vercel.app"
    ]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Credits & Billing
    FREE_TIER_CREDITS: int = 100
    CREDITS_PER_TTS_CHAR: float = 0.001
    CREDITS_PER_SCRIPT_PARSE: int = 5
    CREDITS_PER_VIDEO_RENDER: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()


# Google Cloud credentials setup
def setup_google_credentials():
    """Write Google credentials JSON to file if provided via env var"""
    if settings.GOOGLE_APPLICATION_CREDENTIALS_JSON:
        import json
        credentials_path = "/app/credentials.json"
        with open(credentials_path, "w") as f:
            json.dump(json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON), f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

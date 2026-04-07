"""
app/core/config.py
Application settings loaded from .env via pydantic-settings.
All environment variables are validated and typed here.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────
    APP_NAME: str = "CoalSpark Restaurant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ── Database ─────────────────────────────────────────
    DATABASE_URL: str

    # ── JWT ──────────────────────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ── CORS ─────────────────────────────────────────────
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    # ── Upload ───────────────────────────────────────────
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5 MB

    # ── Razorpay ─────────────────────────────────────────
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance — call this anywhere to access config."""
    # Ensure backend/.env is loaded regardless of current working directory
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    inst = Settings()
    # Debug: print presence of Razorpay keys (masked secret)
    try:
        secret = inst.RAZORPAY_KEY_SECRET or ""
        masked = (secret[:4] + "..." + secret[-4:]) if secret else None
        print(f"Loaded RAZORPAY_KEY_ID={inst.RAZORPAY_KEY_ID}")
        print(f"Loaded RAZORPAY_KEY_SECRET={masked}")
    except Exception:
        pass
    return inst


settings = get_settings()
import os
from pathlib import Path

from dotenv import load_dotenv


# =====================================================
# Base Directory
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

# Load variables from .env
load_dotenv(BASE_DIR / ".env")


# =====================================================
# Base Configuration
# =====================================================

class Config:

    # -------------------------------------
    # Security
    # -------------------------------------

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is not set. "
            "Please create a .env file and define SECRET_KEY."
        )

    # -------------------------------------
    # Database
    # -------------------------------------

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'nsl_platform.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------
    # Upload Settings
    # -------------------------------------

    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "videos"

    PROFILE_IMAGE_FOLDER = (
        BASE_DIR / "app" / "static" / "profile_images"
    )

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

    ALLOWED_VIDEO_EXTENSIONS = {
        "mp4",
        "mov",
        "webm"
    }

    # -------------------------------------
    # Flask Settings
    # -------------------------------------

    DEBUG = False

    TESTING = False


# =====================================================
# Development Configuration
# =====================================================

class DevelopmentConfig(Config):

    DEBUG = True


# =====================================================
# Production Configuration
# =====================================================

class ProductionConfig(Config):

    DEBUG = False


# =====================================================
# Testing Configuration
# =====================================================

class TestingConfig(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{BASE_DIR / 'test.db'}"
    )


# =====================================================
# Configuration Dictionary
# =====================================================

config = {

    "development": DevelopmentConfig,

    "production": ProductionConfig,

    "testing": TestingConfig,

    "default": DevelopmentConfig

}
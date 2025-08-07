from .base import *

# Development settings
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Use SQLite for faster local setup if desired
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Allow all CORS origins in dev
CORS_ALLOW_ALL_ORIGINS = True
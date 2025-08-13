from .base import *

# Development settings
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Use SQLite for faster local setup if desired
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hospital_db',
        'USER': 'hospital_user',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# Allow all CORS origins in dev
CORS_ALLOW_ALL_ORIGINS = True
from .base import *

# Production overrides
DEBUG = False
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", "your.domain.com").split(",")

# Security hardening
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Use env‐configured database (PostgreSQL/MySQL)
# Already defined in base.py via env vars

# Turn off in‐browser error pages
ADMINS = [("Admin", get_env("ADMIN_EMAIL", ""))]
MANAGERS = ADMINS
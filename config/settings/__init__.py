import os
from django.core.exceptions import ImproperlyConfigured

# Choose your switch: either DJANGO_SETTINGS_MODULE or DJANGO_ENVIRONMENT
ENV = os.getenv("DJANGO_ENVIRONMENT", "").lower()
# ENV = os.getenv("DJANGO_SETTINGS_MODULE", "").split('.')[-1]  # alternative

if ENV in ("", "dev", "development"):
    from .dev import *
elif ENV in ("prod", "production"):
    from .prod import *
else:
    raise ImproperlyConfigured(
        f"DJANGO_ENVIRONMENT must be 'dev' or 'prod'; got '{ENV}'."
    )
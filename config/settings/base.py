import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent.parent


load_dotenv()

raw_cors_origins = os.getenv("RAW_CORS_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in raw_cors_origins.split(",")
    if origin.strip()
]


def get_env(var_name, default=None):
    return os.getenv(var_name, default)

# SECURITY
SECRET_KEY = get_env("DJANGO_SECRET_KEY", "change-me-in-production")
DEBUG = get_env("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [host.strip() for host in get_env("ALLOWED_HOSTS", "localhost").split(",") if host.strip()]

# APPLICATION DEFINITION
INSTALLED_APPS = [
    "corsheaders",
    'public',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",

    # Your apps
    
    "apps.patients",
    "apps.appointments",
    "apps.pharmacy",
    "apps.billing",
    "apps.security",
    "apps.doctors",
    "apps.inventory",
    "apps.labs",
    "apps.consultations.apps.ConsultationsConfig",
    "apps.ipd.apps.IpdConfig",
    "apps.users.apps.UsersConfig",
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MIDDLEWARE = [
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Audit & request‐tracking middleware
    #"apps.security.middleware.RequestTrackingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR /"public" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'public.context_processors.role_nav',
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hospital_db',
        'USER': 'hospital_user',  # or 'postgres'
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE':0,
    }
} 

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = get_env("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in get_env("CORS_ALLOWED_ORIGINS", "").split(",") if origin.strip()]

# SimpleJWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(get_env("JWT_ACCESS_LIFETIME", 15))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(get_env("JWT_REFRESH_LIFETIME", 7))),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": get_env("JWT_SECRET", SECRET_KEY),
}

# Custom user model uses the app label from SecurityConfig (label="apps_security")
AUTH_USER_MODEL = "security.User"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        # General Django logs
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',        # was DEBUG
            'propagate': True,
        },
        # Database query logs
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',     # only warn/errors shown
            'propagate': False,
        },
    },
}
LOGIN_URL        = 'security:login'
LOGIN_REDIRECT_URL = 'home'   # fallback
LOGOUT_REDIRECT_URL = 'security:login'
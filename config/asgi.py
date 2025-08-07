import os
from django.core.asgi import get_asgi_application
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
application = get_asgi_application()
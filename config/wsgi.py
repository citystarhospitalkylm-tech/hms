import os
import sys
from django.core.wsgi import get_wsgi_application
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
application = get_wsgi_application()
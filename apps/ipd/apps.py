# apps/ipd/apps.py

from django.apps import AppConfig

class IpdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ipd'

    def ready(self):
        # Use a relative import so this is loaded as apps.ipd.signals
        from . import signals
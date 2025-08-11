from django.apps import AppConfig

class SecurityConfig(AppConfig):
    # This must match the import path of your app directory
    name = 'apps.security'
    # This is the “short” name Django uses to refer to your app
    label = 'security'
    verbose_name = 'Security'

    def ready(self):
        # Import signals by full Python path
        import apps.security.signals  # noqa

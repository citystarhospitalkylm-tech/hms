from django.apps import AppConfig


class SecurityConfig(AppConfig):
    name = "apps.security"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Security & Audit"

    def ready(self):
        if not hasattr(self, "_signals_loaded"):
            import security.signals  # noqa
            self._signals_loaded = True

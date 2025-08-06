from django.apps import AppConfig

class InventoryConfig(AppConfig):
    name = 'apps.inventory'

    def ready(self):
        # ensure signal registration
        import apps.inventory.signals  # noqa
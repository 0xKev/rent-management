from django.apps import AppConfig

default_app_config = 'rent_management.apps.RentManagementConfig'  

class RentManagementConfig(AppConfig):
    name = 'rent_management'

    def ready(self):
        import rent_management.signals   # Ensure signals.py is loaded

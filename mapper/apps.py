from django.apps import AppConfig


class MapperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mapper'
    
    def ready(self):
        import mapper.signals  # Import the signals to connect them

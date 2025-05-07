"""
Application configuration for the 'mapper' app.

Defines the MapperConfig AppConfig subclass, setting the default auto field
and registering model signal handlers on startup.

ready():
    Imports mapper.signals so that Report photo cleanup handlers (pre_save and
    post_delete) are connected when the application loads.
"""
from django.apps import AppConfig

class MapperConfig(AppConfig):
    """
    AppConfig for the 'mapper' application.

    - Sets the default primary key field type to BigAutoField.
    - On ready(), imports mapper.signals to register Report photo cleanup handlers.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mapper'

    def ready(self):
        # Import the signals to connect them
        import mapper.signals  

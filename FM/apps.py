from django.apps import AppConfig

class FmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FM'

    def ready(self):
        import FM.signals

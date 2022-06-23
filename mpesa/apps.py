from django.apps import AppConfig


class MpesaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mpesa'

    def ready(self) -> None:
        from .scheduler import start
        start()

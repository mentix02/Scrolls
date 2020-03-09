from django.apps import AppConfig


class ParchmentConfig(AppConfig):
    name = 'parchment'

    def ready(self):
        import parchment.signals

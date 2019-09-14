from django.apps import AppConfig


class DigitaldairyConfig(AppConfig):
    name = 'digitaldairy'

    def ready(self):
        from .events_updater import send_push_messages
        send_push_messages.start()
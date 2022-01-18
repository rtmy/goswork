from django.apps import AppConfig
from django.db.models.signals import pre_save


class TelegrammeConfig(AppConfig):
    name = 'telegramme'

    def ready(self):
        with open('statefile', 'w') as file:
            file.write('0')

from django.apps import AppConfig


class MyadminConfig(AppConfig):
    name = 'myadmin'

    def ready(self):
        print('myadmin ready')

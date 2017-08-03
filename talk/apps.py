from django.apps import AppConfig
import talk


class TalkConfig(AppConfig):
    name = 'talk'

    def ready(self):
        import talk.signal

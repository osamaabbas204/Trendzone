from django.apps import AppConfig


class TrendzConfig(AppConfig):
    name = 'Trendz'

    def ready(self):
        from . import scheduleData
        scheduleData.start()

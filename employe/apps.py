from django.apps import AppConfig
from django.db.models.signals import post_migrate


class EmployeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employe'

    def ready(self):
        from employe.signal import create_initial_records

        post_migrate.connect(create_initial_records, sender=self)

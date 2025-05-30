# custom_celery_beat/apps.py
from django.apps import AppConfig

class BeatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_celery_beat'  # 'django_celery_beat' emas
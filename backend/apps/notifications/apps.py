"""
BLACK LIGHT Collective — Notifications / AppConfig
Konfiguracja aplikacji powiadomień i emaili.
"""
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Konfiguracja aplikacji powiadomień."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'
    verbose_name = 'Powiadomienia'

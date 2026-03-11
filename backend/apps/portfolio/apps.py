"""
BLACK LIGHT Collective — Portfolio / AppConfig
Konfiguracja aplikacji portfolio — realizacje, zespół, opinie.
"""
from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    """Konfiguracja aplikacji portfolio."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'
    verbose_name = 'Portfolio'

"""
BLACK LIGHT Collective — Configurator / AppConfig
Konfiguracja aplikacji konfiguratora scen festiwalowych.
"""
from django.apps import AppConfig


class ConfiguratorConfig(AppConfig):
    """Konfiguracja aplikacji konfiguratora scen."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.configurator'
    verbose_name = 'Konfigurator scen'

"""
BLACK LIGHT Collective — Scene Builder 3D / AppConfig
Konfiguracja aplikacji interaktywnego edytora scen 3D.
"""
from django.apps import AppConfig


class ScenebuilderConfig(AppConfig):
    """Konfiguracja aplikacji edytora scen 3D."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.scenebuilder'
    verbose_name = 'Scene Builder 3D'

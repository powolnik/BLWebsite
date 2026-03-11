"""
BLACK LIGHT Collective — Accounts / AppConfig
Konfiguracja aplikacji Django odpowiedzialnej za konta użytkowników.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Konfiguracja aplikacji kont użytkowników."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Konta'

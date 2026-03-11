"""
BLACK LIGHT Collective — Shop / AppConfig
Konfiguracja aplikacji sklepu — produkty, koszyk, zamówienia, płatności.
"""
from django.apps import AppConfig


class ShopConfig(AppConfig):
    """Konfiguracja aplikacji sklepu."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.shop'
    verbose_name = 'Sklep'

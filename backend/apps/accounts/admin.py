"""
BLACK LIGHT Collective — Accounts / Admin
Konfiguracja panelu administracyjnego dla użytkowników i adresów.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserAddress


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Panel admina z dodatkowymi polami profilu BLACK LIGHT."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined']
    # Rozszerzamy domyślne fieldsets Django o sekcję z polami platformy
    fieldsets = UserAdmin.fieldsets + (
        ('Dodatkowe', {'fields': ('phone', 'avatar', 'bio', 'role', 'company', 'website')}),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """Panel admina adresów użytkowników."""
    list_display = ['user', 'label', 'city', 'is_default']
    list_filter = ['city', 'is_default']

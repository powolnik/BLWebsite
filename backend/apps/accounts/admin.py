from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserAddress


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Dodatkowe', {'fields': ('phone', 'avatar', 'bio', 'role', 'company', 'website')}),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'is_default']
    list_filter = ['city', 'is_default']

"""
BLACK LIGHT Collective — Configurator / Admin
Panel administracyjny konfiguratora: szablony, kategorie, komponenty, zamówienia.
"""
from django.contrib import admin

from .models import SceneTemplate, ComponentCategory, Component, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline elementów zamówienia w panelu zamówienia."""
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'subtotal']


@admin.register(SceneTemplate)
class SceneTemplateAdmin(admin.ModelAdmin):
    """Panel admina szablonów scen z auto-generowanym slugiem."""
    list_display = ['name', 'base_price', 'width', 'depth', 'height', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'base_price', 'is_active')}),
        ('Obrazek', {'fields': ('preview_image', 'thumbnail_url')}),
        ('Wymiary', {'fields': ('width', 'depth', 'height')}),
    )


@admin.register(ComponentCategory)
class ComponentCategoryAdmin(admin.ModelAdmin):
    """Panel admina kategorii komponentów z edytowalną kolejnością i kolorem."""
    list_display = ['name', 'icon', 'color', 'order']
    list_editable = ['order', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    """Panel admina komponentów sceny z wyszukiwarką i filtrami."""
    list_display = ['name', 'category', 'price', 'icon_name', 'is_available', 'power_consumption']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'description', 'short_desc', 'price')}),
        ('Wizualizacja', {'fields': ('image', 'thumbnail_url', 'icon_name', 'color')}),
        ('Wymiary i specyfikacja', {'fields': ('width_m', 'depth_m', 'weight_kg', 'power_consumption', 'specs')}),
        ('Dostępność', {'fields': ('is_available', 'max_quantity')}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Panel admina zamówień z hierarchią dat i inline elementami."""
    list_display = ['__str__', 'user', 'status', 'event_date', 'total_price', 'created_at']
    list_filter = ['status', 'event_date']
    search_fields = ['event_name', 'user__username', 'user__email']
    inlines = [OrderItemInline]
    readonly_fields = ['subtotal', 'template_price', 'total_price']
    date_hierarchy = 'created_at'

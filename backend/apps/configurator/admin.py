from django.contrib import admin
from .models import SceneTemplate, ComponentCategory, Component, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_price', 'subtotal']


@admin.register(SceneTemplate)
class SceneTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_price', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ComponentCategory)
class ComponentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'power_consumption']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'event_date', 'total_price', 'created_at']
    list_filter = ['status', 'event_date']
    search_fields = ['event_name', 'user__username', 'user__email']
    inlines = [OrderItemInline]
    readonly_fields = ['subtotal', 'template_price', 'total_price']
    date_hierarchy = 'created_at'

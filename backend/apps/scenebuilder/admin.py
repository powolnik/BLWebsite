"""
BLACK LIGHT Collective — Scene Builder 3D / Admin
Panel administracyjny edytora scen 3D: kategorie, modele, sceny.
"""
from django.contrib import admin

from .models import Model3D, Model3DCategory, Scene


@admin.register(Model3DCategory)
class Model3DCategoryAdmin(admin.ModelAdmin):
    """Panel admina kategorii modeli 3D z auto-generowanym slugiem."""
    list_display = ['name', 'icon', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    """Panel admina modeli 3D — wymiary, cena, pobór mocy."""
    list_display = [
        'name', 'category', 'slug', 'bbox_width', 'bbox_height', 'bbox_depth',
        'weight', 'price_per_unit', 'power_consumption', 'is_active', 'created_at',
    ]
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['category__order', 'name']


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    """Panel admina scen — wymiary siatki, status publiczności."""
    list_display = [
        'name', 'slug', 'user', 'is_public',
        'grid_width', 'grid_height', 'grid_depth',
        'created_at', 'updated_at',
    ]
    list_filter = ['is_public']
    search_fields = ['name', 'slug', 'description']
    ordering = ['-updated_at']

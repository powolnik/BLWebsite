"""
BLACK LIGHT Collective — Scene Builder 3D / Models
Modele interaktywnego edytora scen 3D.
Zawiera: kategorie modeli 3D, same modele (GLB/GLTF),
oraz sceny użytkowników z danymi binarnymi (format BL3D) i JSON.
"""
from django.conf import settings
from django.db import models


class Model3DCategory(models.Model):
    """Kategoria modeli 3D (np. Lighting, Staging, Audio, Effects).

    Służy do organizacji biblioteki modeli w edytorze 3D.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, help_text='Emoji icon for the category')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = '3D Model Category'
        verbose_name_plural = '3D Model Categories'

    def __str__(self):
        return f'{self.icon} {self.name}'


class Model3D(models.Model):
    """Model 3D (plik GLB/GLTF) dostępny w bibliotece edytora.

    Przechowuje plik modelu, wymiary bounding box (cm), wagę,
    cenę jednostkową i maksymalną liczbę instancji na scenę.
    """
    category = models.ForeignKey(
        Model3DCategory,
        on_delete=models.CASCADE,
        related_name='models',
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to='models3d/', help_text='GLB/GLTF file')
    thumbnail = models.ImageField(upload_to='models3d/thumbs/', blank=True, null=True)

    # Bounding box dimensions in centimeters
    bbox_width = models.FloatField(help_text='Bounding box width in cm')
    bbox_height = models.FloatField(help_text='Bounding box height in cm')
    bbox_depth = models.FloatField(help_text='Bounding box depth in cm')

    weight = models.FloatField(default=0, help_text='Weight in kg')
    max_instances = models.IntegerField(default=10, help_text='Max instances per scene')
    price_per_unit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text='Price per unit'
    )
    power_consumption = models.FloatField(default=0, help_text='Power consumption in watts')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'name']
        verbose_name = '3D Model'
        verbose_name_plural = '3D Models'

    def __str__(self):
        return self.name


class Scene(models.Model):
    """Zapisana scena użytkownika z rozmieszczonymi modelami 3D.

    Przechowuje konfigurację sceny w dwóch formatach:
    - scene_data: dane binarne w formacie BL3D (natywny eksport)
    - scene_json: fallback JSON z pozycjami obiektów

    Wymiary siatki (grid) w centymetrach. Sceny mogą być publiczne.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scenes',
        null=True,
        blank=True,
        help_text='Owner of the scene (null for anonymous)',
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    # Grid dimensions in centimeters
    grid_width = models.FloatField(default=2000, help_text='Grid width in cm (default 20m)')
    grid_height = models.FloatField(default=1000, help_text='Grid height in cm (default 10m)')
    grid_depth = models.FloatField(default=2000, help_text='Grid depth in cm (default 20m)')

    # Scene data storage — dual format for flexibility
    scene_data = models.BinaryField(
        blank=True, null=True, help_text='Serialized scene binary (BL3D format)'
    )
    scene_json = models.JSONField(
        default=dict, help_text='JSON fallback of scene objects'
    )

    thumbnail = models.ImageField(upload_to='scenes/thumbs/', blank=True, null=True)
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Scene'
        verbose_name_plural = 'Scenes'

    def __str__(self):
        return self.name

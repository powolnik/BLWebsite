from django.db import models
from django.conf import settings


class SceneTemplate(models.Model):
    """Szablon sceny (np. Main Stage, Techno Cave, Forest Stage)."""
    name = models.CharField('Nazwa', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Opis')
    base_price = models.DecimalField('Cena bazowa', max_digits=10, decimal_places=2)
    preview_image = models.ImageField('Podglad', upload_to='templates/')
    model_3d_url = models.URLField('URL modelu 3D', blank=True)
    width = models.DecimalField('Szerokosc (m)', max_digits=6, decimal_places=2, default=10)
    depth = models.DecimalField('Glebokosc (m)', max_digits=6, decimal_places=2, default=8)
    height = models.DecimalField('Wysokosc (m)', max_digits=6, decimal_places=2, default=6)
    is_active = models.BooleanField('Aktywny', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Szablon sceny'
        verbose_name_plural = 'Szablony scen'
        ordering = ['name']

    def __str__(self):
        return self.name


class ComponentCategory(models.Model):
    """Kategoria komponentow: Oswietlenie, Dekoracje, Dzwiek, Efekty specjalne."""
    name = models.CharField('Nazwa', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    icon = models.CharField('Ikona (CSS class)', max_length=50, blank=True)
    description = models.TextField('Opis', blank=True)
    order = models.PositiveIntegerField('Kolejnosc', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Kategoria komponentow'
        verbose_name_plural = 'Kategorie komponentow'

    def __str__(self):
        return self.name


class Component(models.Model):
    """Pojedynczy element do wyboru w kreatorze."""
    category = models.ForeignKey(
        ComponentCategory, on_delete=models.CASCADE, related_name='components'
    )
    name = models.CharField('Nazwa', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Opis')
    price = models.DecimalField('Cena', max_digits=10, decimal_places=2)
    image = models.ImageField('Zdjecie', upload_to='components/')
    specs = models.JSONField('Specyfikacja techniczna', default=dict, blank=True)
    power_consumption = models.PositiveIntegerField('Pobor mocy (W)', default=0)
    weight_kg = models.DecimalField('Waga (kg)', max_digits=6, decimal_places=2, default=0)
    is_available = models.BooleanField('Dostepny', default=True)
    max_quantity = models.PositiveIntegerField('Maks. ilosc', default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Komponent'
        verbose_name_plural = 'Komponenty'

    def __str__(self):
        return f'{self.category.name} > {self.name}'


class Order(models.Model):
    """Zamowienie konfiguracji sceny od klienta."""
    STATUS_CHOICES = [
        ('draft', 'Szkic'),
        ('submitted', 'Zlozone'),
        ('reviewed', 'W recenzji'),
        ('quoted', 'Wycenione'),
        ('accepted', 'Zaakceptowane'),
        ('in_progress', 'W realizacji'),
        ('completed', 'Zrealizowane'),
        ('cancelled', 'Anulowane'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='scene_orders', verbose_name='Uzytkownik'
    )
    template = models.ForeignKey(
        SceneTemplate, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders', verbose_name='Szablon'
    )
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='draft')

    # Event details
    event_name = models.CharField('Nazwa wydarzenia', max_length=300)
    event_date = models.DateField('Data wydarzenia')
    event_end_date = models.DateField('Data zakonczenia', null=True, blank=True)
    event_location = models.CharField('Lokalizacja', max_length=500)
    expected_audience = models.PositiveIntegerField('Przewidywana publicznosc', default=0)

    # Pricing
    subtotal = models.DecimalField('Kwota komponentow', max_digits=12, decimal_places=2, default=0)
    template_price = models.DecimalField('Cena szablonu', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Rabat', max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField('Cena calkowita', max_digits=12, decimal_places=2, default=0)

    notes = models.TextField('Uwagi klienta', blank=True)
    internal_notes = models.TextField('Notatki wewnetrzne', blank=True)
    scene_data = models.JSONField('Dane konfiguracji sceny', default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Zamowienie sceny'
        verbose_name_plural = 'Zamowienia scen'

    def __str__(self):
        return f'#{self.pk} - {self.event_name} ({self.get_status_display()})'

    def recalculate_total(self):
        """Przelicz calkowita kwote zamowienia."""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.template_price = self.template.base_price if self.template else 0
        self.total_price = self.subtotal + self.template_price - self.discount
        self.save(update_fields=['subtotal', 'template_price', 'total_price'])


class OrderItem(models.Model):
    """Wybrany komponent w zamowieniu."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Ilosc', default=1)
    unit_price = models.DecimalField('Cena jednostkowa', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Kwota', max_digits=10, decimal_places=2)
    position_data = models.JSONField('Pozycja na scenie (x,y,z)', default=dict, blank=True)
    notes = models.CharField('Uwagi', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Element zamowienia'
        verbose_name_plural = 'Elementy zamowienia'

    def __str__(self):
        return f'{self.component.name} x{self.quantity}'

    def save(self, *args, **kwargs):
        self.unit_price = self.component.price
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

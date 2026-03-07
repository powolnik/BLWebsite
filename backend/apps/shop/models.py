from django.db import models
from django.conf import settings


class ProductCategory(models.Model):
    """Kategoria produktow w sklepie."""
    name = models.CharField('Nazwa', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Opis', blank=True)
    image = models.ImageField('Zdjecie', upload_to='shop/categories/', blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name='Kategoria nadrzedna'
    )
    order = models.PositiveIntegerField('Kolejnosc', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Kategoria produktu'
        verbose_name_plural = 'Kategorie produktow'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produkt w sklepie (merch, elementy scen, akcesoria)."""
    name = models.CharField('Nazwa', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='products'
    )
    description = models.TextField('Opis')
    short_description = models.CharField('Krotki opis', max_length=500, blank=True)
    price = models.DecimalField('Cena', max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(
        'Cena przed rabatem', max_digits=10, decimal_places=2, null=True, blank=True
    )
    sku = models.CharField('SKU', max_length=50, unique=True, blank=True)
    stock = models.PositiveIntegerField('Stan magazynowy', default=0)
    is_active = models.BooleanField('Aktywny', default=True)
    is_featured = models.BooleanField('Wyrozniany', default=False)
    weight_kg = models.DecimalField('Waga (kg)', max_digits=6, decimal_places=2, default=0)
    tags = models.CharField('Tagi (oddzielone przecinkiem)', max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img.image if img else None


class ProductImage(models.Model):
    """Zdjecie produktu."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Zdjecie', upload_to='shop/products/')
    alt_text = models.CharField('Tekst alternatywny', max_length=200, blank=True)
    is_primary = models.BooleanField('Glowne zdjecie', default=False)
    order = models.PositiveIntegerField('Kolejnosc', default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} - img {self.order}'


class Cart(models.Model):
    """Koszyk zakupowy."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name='cart'
    )
    session_key = models.CharField('Klucz sesji', max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Koszyk'
        verbose_name_plural = 'Koszyki'

    def __str__(self):
        owner = self.user.username if self.user else f'sesja:{self.session_key[:8]}'
        return f'Koszyk ({owner})'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Element koszyka."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Ilosc', default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Element koszyka'
        verbose_name_plural = 'Elementy koszyka'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class ShopOrder(models.Model):
    """Zamowienie ze sklepu."""
    STATUS_CHOICES = [
        ('pending', 'Oczekuje'),
        ('paid', 'Oplacone'),
        ('processing', 'W realizacji'),
        ('shipped', 'Wyslane'),
        ('delivered', 'Dostarczone'),
        ('cancelled', 'Anulowane'),
        ('refunded', 'Zwrocone'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='shop_orders'
    )
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField('Suma', max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField('Koszt wysylki', max_digits=8, decimal_places=2, default=0)
    discount = models.DecimalField('Rabat', max_digits=10, decimal_places=2, default=0)

    # Shipping info
    shipping_name = models.CharField('Imie i nazwisko', max_length=200)
    shipping_street = models.CharField('Ulica', max_length=300)
    shipping_city = models.CharField('Miasto', max_length=100)
    shipping_postal_code = models.CharField('Kod pocztowy', max_length=10)
    shipping_country = models.CharField('Kraj', max_length=100, default='Polska')
    tracking_number = models.CharField('Numer sledzenia', max_length=100, blank=True)

    notes = models.TextField('Uwagi', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Zamowienie sklepowe'
        verbose_name_plural = 'Zamowienia sklepowe'

    def __str__(self):
        return f'Zamowienie #{self.pk} - {self.get_status_display()}'

    @property
    def grand_total(self):
        return self.total + self.shipping_cost - self.discount


class ShopOrderItem(models.Model):
    """Element zamowienia sklepowego."""
    order = models.ForeignKey(ShopOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField('Nazwa produktu', max_length=300)
    quantity = models.PositiveIntegerField('Ilosc')
    unit_price = models.DecimalField('Cena jednostkowa', max_digits=10, decimal_places=2)
    subtotal = models.DecimalField('Kwota', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'


class Payment(models.Model):
    """Platnosc (Stripe / PayU / Przelewy24)."""
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('payu', 'PayU'),
        ('p24', 'Przelewy24'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Oczekuje'),
        ('completed', 'Zrealizowana'),
        ('failed', 'Nieudana'),
        ('refunded', 'Zwrocona'),
    ]

    shop_order = models.ForeignKey(
        ShopOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='payments'
    )
    scene_order = models.ForeignKey(
        'configurator.Order', on_delete=models.CASCADE, null=True, blank=True,
        related_name='payments'
    )
    amount = models.DecimalField('Kwota', max_digits=12, decimal_places=2)
    currency = models.CharField('Waluta', max_length=3, default='PLN')
    provider = models.CharField('Dostawca', max_length=10, choices=PROVIDER_CHOICES)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pending')
    external_id = models.CharField('ID zewnetrzny', max_length=200, blank=True)
    metadata = models.JSONField('Metadane', default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Platnosc'
        verbose_name_plural = 'Platnosci'

    def __str__(self):
        return f'{self.provider} - {self.amount} {self.currency} ({self.get_status_display()})'


class Coupon(models.Model):
    """Kupon rabatowy."""
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Procentowy'),
        ('fixed', 'Kwotowy'),
    ]

    code = models.CharField('Kod', max_length=50, unique=True)
    discount_type = models.CharField('Typ rabatu', max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField('Wartosc rabatu', max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(
        'Min. kwota zamowienia', max_digits=10, decimal_places=2, default=0
    )
    max_uses = models.PositiveIntegerField('Maks. uzyc', default=0)
    times_used = models.PositiveIntegerField('Uzyto razy', default=0)
    valid_from = models.DateTimeField('Wazny od')
    valid_until = models.DateTimeField('Wazny do')
    is_active = models.BooleanField('Aktywny', default=True)

    class Meta:
        verbose_name = 'Kupon'
        verbose_name_plural = 'Kupony'

    def __str__(self):
        return self.code

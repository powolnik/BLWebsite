from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Rozszerzony model uzytkownika."""
    ROLE_CHOICES = [
        ('client', 'Klient'),
        ('member', 'Czlonek zespolu'),
        ('admin', 'Administrator'),
    ]
    phone = models.CharField('Telefon', max_length=20, blank=True)
    avatar = models.ImageField('Awatar', upload_to='avatars/', blank=True)
    bio = models.TextField('Bio', blank=True)
    role = models.CharField('Rola', max_length=10, choices=ROLE_CHOICES, default='client')
    company = models.CharField('Firma', max_length=200, blank=True)
    website = models.URLField('Strona WWW', blank=True)

    class Meta:
        verbose_name = 'Uzytkownik'
        verbose_name_plural = 'Uzytkownicy'
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name() or self.username


class UserAddress(models.Model):
    """Adres uzytkownika (do zamowien i wysylek)."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField('Etykieta', max_length=50, default='Domowy')
    street = models.CharField('Ulica', max_length=300)
    city = models.CharField('Miasto', max_length=100)
    postal_code = models.CharField('Kod pocztowy', max_length=10)
    country = models.CharField('Kraj', max_length=100, default='Polska')
    is_default = models.BooleanField('Domyslny', default=False)

    class Meta:
        verbose_name = 'Adres'
        verbose_name_plural = 'Adresy'

    def __str__(self):
        return f'{self.label}: {self.street}, {self.city}'

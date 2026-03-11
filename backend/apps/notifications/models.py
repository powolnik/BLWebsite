"""
BLACK LIGHT Collective — Notifications / Models
Modele powiadomień i logów emaili.
Notification przechowuje wewnętrzne powiadomienia użytkownika,
EmailLog rejestruje historię wysłanych wiadomości email.
"""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Powiadomienie dla użytkownika.

    Typy: status zamówienia, nowe zamówienie, płatność, systemowe, promocja.
    Pole `link` opcjonalnie kieruje do powiązanego zasobu w aplikacji.
    """
    TYPE_CHOICES = [
        ('order_status', 'Status zamowienia'),
        ('order_new', 'Nowe zamowienie'),
        ('payment', 'Platnosc'),
        ('system', 'Systemowe'),
        ('promo', 'Promocja'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField('Typ', max_length=15, choices=TYPE_CHOICES)
    title = models.CharField('Tytul', max_length=300)
    message = models.TextField('Wiadomosc')
    is_read = models.BooleanField('Przeczytane', default=False)
    link = models.CharField('Link', max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Powiadomienie'
        verbose_name_plural = 'Powiadomienia'

    def __str__(self):
        return f'{self.title} -> {self.user.username}'


class EmailLog(models.Model):
    """Log wysłanych emaili.

    Śledzi status wysyłki: w kolejce → wysłany / nieudany.
    Przechowuje treść i ewentualny komunikat błędu.
    """
    STATUS_CHOICES = [
        ('sent', 'Wyslany'),
        ('failed', 'Nieudany'),
        ('queued', 'W kolejce'),
    ]

    recipient = models.EmailField('Odbiorca')
    subject = models.CharField('Temat', max_length=500)
    body = models.TextField('Tresc')
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='queued')
    error_message = models.TextField('Komunikat bledu', blank=True)
    sent_at = models.DateTimeField('Wyslano', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Log emaila'
        verbose_name_plural = 'Logi emaili'

    def __str__(self):
        return f'{self.subject} -> {self.recipient}'

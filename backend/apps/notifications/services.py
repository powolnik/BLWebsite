"""
BLACK LIGHT Collective — Notifications / Services
Serwis powiadomień — tworzy powiadomienia wewnętrzne,
oznacza je jako przeczytane oraz wysyła emaile z logowaniem.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Notification, EmailLog


class NotificationService:
    """Serwis powiadomień — warstwa biznesowa."""

    @staticmethod
    def create(user, notification_type, title, message, link=''):
        """Utwórz nowe powiadomienie wewnętrzne dla użytkownika."""
        return Notification.objects.create(
            user=user, type=notification_type,
            title=title, message=message, link=link,
        )

    @staticmethod
    def mark_as_read(user, notification_ids=None):
        """Oznacz powiadomienia jako przeczytane.

        Args:
            user: użytkownik, którego powiadomienia oznaczamy
            notification_ids: opcjonalna lista PK do oznaczenia (None = wszystkie)
        """
        qs = Notification.objects.filter(user=user, is_read=False)
        if notification_ids:
            qs = qs.filter(pk__in=notification_ids)
        return qs.update(is_read=True)

    @staticmethod
    def send_email(recipient, subject, body):
        """Wyślij email i zapisz log wyniku (sent/failed).

        Tworzy rekord EmailLog przed wysyłką, następnie aktualizuje
        status w zależności od powodzenia operacji.
        """
        log = EmailLog.objects.create(
            recipient=recipient, subject=subject, body=body,
        )
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
            log.status = 'sent'
            log.sent_at = timezone.now()
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
        log.save()
        return log

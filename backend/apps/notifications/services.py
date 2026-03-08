from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Notification, EmailLog


class NotificationService:
    """Serwis powiadomien."""

    @staticmethod
    def create(user, notification_type, title, message, link=''):
        return Notification.objects.create(
            user=user, type=notification_type,
            title=title, message=message, link=link,
        )

    @staticmethod
    def mark_as_read(user, notification_ids=None):
        qs = Notification.objects.filter(user=user, is_read=False)
        if notification_ids:
            qs = qs.filter(pk__in=notification_ids)
        return qs.update(is_read=True)

    @staticmethod
    def send_email(recipient, subject, body):
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

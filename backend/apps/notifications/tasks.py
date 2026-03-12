"""
BLACK LIGHT Collective — Notifications / Tasks
Zadania Celery do asynchronicznej wysyłki emaili
potwierdzających zamówienia i aktualizacji statusów.
"""
from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id):
    """Wyślij email potwierdzający zamówienie ze sklepu."""
    from .services import NotificationService
    from apps.shop.models import ShopOrder

    order = ShopOrder.objects.select_related('user').get(pk=order_id)
    subject = f'Potwierdzenie zamowienia #{order.pk}'
    body = (
        f'Czesc {order.user.first_name},\n\n'
        f'Twoje zamowienie ze sklepu zostalo zlozone.\n'
        f'Kwota: {order.grand_total} PLN\n\n'
        f'Zespol BLACK LIGHT Collective'
    )

    NotificationService.send_email(order.user.email, subject, body)
    NotificationService.create(
        user=order.user,
        notification_type='order_new',
        title=subject,
        message=body,
    )


@shared_task
def send_order_status_update(order_id, new_status=''):
    """Wyślij powiadomienie o zmianie statusu zamówienia."""
    from .services import NotificationService
    from apps.shop.models import ShopOrder

    order = ShopOrder.objects.select_related('user').get(pk=order_id)
    title = f'Zmiana statusu zamowienia #{order.pk}'
    message = f'Nowy status: {new_status}'

    NotificationService.create(
        user=order.user,
        notification_type='order_status',
        title=title,
        message=message,
    )
    NotificationService.send_email(order.user.email, title, message)

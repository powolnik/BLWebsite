"""
BLACK LIGHT Collective — Notifications / Tasks
Zadania Celery do asynchronicznej wysyłki emaili
potwierdzających zamówienia i aktualizacji statusów.
"""
from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id, order_type='scene'):
    """Wyślij email potwierdzający zamówienie (scena lub sklep).

    Importy wewnątrz funkcji — unikamy cyklicznych zależności
    i zapewniamy lazy-loading modeli w kontekście workera Celery.
    """
    from .services import NotificationService

    if order_type == 'scene':
        # Zamówienie konfiguracji sceny
        from apps.configurator.models import Order
        order = Order.objects.select_related('user').get(pk=order_id)
        subject = f'Potwierdzenie zamowienia sceny #{order.pk}'
        body = (
            f'Czesc {order.user.first_name},\n\n'
            f'Twoje zamowienie sceny na {order.event_name} zostalo zlozone.\n'
            f'Status: {order.get_status_display()}\n'
            f'Kwota: {order.total_price} PLN\n\n'
            f'Zespol BLACK LIGHT Collective'
        )
    else:
        # Zamówienie ze sklepu
        from apps.shop.models import ShopOrder
        order = ShopOrder.objects.select_related('user').get(pk=order_id)
        subject = f'Potwierdzenie zamowienia #{order.pk}'
        body = (
            f'Czesc {order.user.first_name},\n\n'
            f'Twoje zamowienie ze sklepu zostalo zlozone.\n'
            f'Kwota: {order.grand_total} PLN\n\n'
            f'Zespol BLACK LIGHT Collective'
        )

    # Wyślij email i utwórz powiadomienie wewnętrzne
    NotificationService.send_email(order.user.email, subject, body)
    NotificationService.create(
        user=order.user,
        notification_type='order_new',
        title=subject,
        message=body,
    )


@shared_task
def send_order_status_update(order_id, order_type='scene', new_status=''):
    """Wyślij powiadomienie o zmianie statusu zamówienia.

    Obsługuje oba typy zamówień: sceny i sklep.
    Tworzy powiadomienie wewnętrzne + wysyła email.
    """
    from .services import NotificationService

    if order_type == 'scene':
        from apps.configurator.models import Order
        order = Order.objects.select_related('user').get(pk=order_id)
        title = f'Zmiana statusu zamowienia sceny #{order.pk}'
    else:
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

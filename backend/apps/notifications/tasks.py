from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id, order_type='scene'):
    """Wyslij email potwierdzajacy zamowienie."""
    from .services import NotificationService

    if order_type == 'scene':
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
def send_order_status_update(order_id, order_type='scene', new_status=''):
    """Wyslij powiadomienie o zmianie statusu."""
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

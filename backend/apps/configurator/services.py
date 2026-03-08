from decimal import Decimal
from .models import Order, OrderItem, Component


class ConfiguratorService:
    """Logika biznesowa konfiguratora scen."""

    @staticmethod
    def add_item(order: Order, component_id: int, quantity: int = 1,
                 position_data: dict = None) -> OrderItem:
        """Dodaj komponent do zamowienia."""
        component = Component.objects.get(pk=component_id, is_available=True)
        item, created = OrderItem.objects.get_or_create(
            order=order, component=component,
            defaults={
                'quantity': quantity,
                'unit_price': component.price,
                'subtotal': component.price * quantity,
                'position_data': position_data or {},
            }
        )
        if not created:
            item.quantity += quantity
            item.subtotal = item.unit_price * item.quantity
            item.save()
        order.recalculate_total()
        return item

    @staticmethod
    def remove_item(order: Order, item_id: int) -> None:
        """Usun komponent z zamowienia."""
        OrderItem.objects.filter(pk=item_id, order=order).delete()
        order.recalculate_total()

    @staticmethod
    def update_item_quantity(order: Order, item_id: int, quantity: int) -> OrderItem:
        """Zmien ilosc komponentu."""
        item = OrderItem.objects.get(pk=item_id, order=order)
        if quantity <= 0:
            item.delete()
            order.recalculate_total()
            return None
        item.quantity = quantity
        item.save()
        order.recalculate_total()
        return item

    @staticmethod
    def submit_order(order: Order) -> Order:
        """Zloze zamowienie do recenzji."""
        if order.status != 'draft':
            raise ValueError('Tylko szkic moze byc zlozony.')
        if not order.items.exists():
            raise ValueError('Zamowienie musi zawierac min. 1 element.')
        order.status = 'submitted'
        order.save(update_fields=['status'])
        return order

    @staticmethod
    def calculate_power_summary(order: Order) -> dict:
        """Podsumowanie zuzycia mocy."""
        items = order.items.select_related('component').all()
        total_power = sum(
            item.component.power_consumption * item.quantity for item in items
        )
        total_weight = sum(
            float(item.component.weight_kg) * item.quantity for item in items
        )
        return {
            'total_power_watts': total_power,
            'total_weight_kg': round(total_weight, 2),
            'item_count': sum(item.quantity for item in items),
        }

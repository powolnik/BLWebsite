"""
BLACK LIGHT Collective — Configurator / Services
Warstwa logiki biznesowej konfiguratora scen.
Odpowiada za dodawanie/usuwanie elementów zamówienia,
składanie zamówień i obliczanie podsumowań technicznych.
"""
from .models import Order, OrderItem, Component


class ConfiguratorService:
    """Logika biznesowa konfiguratora scen."""

    @staticmethod
    def add_item(order: Order, component_id: int, quantity: int = 1,
                 position_data: dict = None) -> OrderItem:
        """Dodaj komponent do zamówienia.

        Jeśli komponent już istnieje w zamówieniu, zwiększa ilość.
        Po dodaniu przelicza total zamówienia.
        """
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
            # Komponent już w zamówieniu — zwiększ ilość
            item.quantity += quantity
            item.subtotal = item.unit_price * item.quantity
            item.save()
        order.recalculate_total()
        return item

    @staticmethod
    def remove_item(order: Order, item_id: int) -> None:
        """Usuń komponent z zamówienia i przelicz total."""
        OrderItem.objects.filter(pk=item_id, order=order).delete()
        order.recalculate_total()

    @staticmethod
    def update_item_quantity(order: Order, item_id: int, quantity: int) -> OrderItem:
        """Zmień ilość komponentu. Jeśli quantity <= 0, usuwa element."""
        item = OrderItem.objects.get(pk=item_id, order=order)
        if quantity <= 0:
            item.delete()
            order.recalculate_total()
            return None
        item.quantity = quantity
        item.save()  # save() automatycznie przelicza subtotal
        order.recalculate_total()
        return item

    @staticmethod
    def submit_order(order: Order) -> Order:
        """Złóż zamówienie do recenzji.

        Warunki: status musi być 'draft' i zamówienie musi zawierać min. 1 element.
        """
        if order.status != 'draft':
            raise ValueError('Tylko szkic moze byc zlozony.')
        if not order.items.exists():
            raise ValueError('Zamowienie musi zawierac min. 1 element.')
        order.status = 'submitted'
        order.save(update_fields=['status'])
        return order

    @staticmethod
    def calculate_power_summary(order: Order) -> dict:
        """Podsumowanie zużycia mocy (W) i wagi (kg) zamówienia.

        Returns:
            dict z kluczami: total_power_watts, total_weight_kg, item_count
        """
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

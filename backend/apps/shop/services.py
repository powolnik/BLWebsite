"""
BLACK LIGHT Collective — Shop / Services
Warstwa logiki biznesowej sklepu: zarządzanie koszykiem,
składanie zamówień (checkout) i walidacja kuponów rabatowych.
"""
from decimal import Decimal

from django.utils import timezone

from .models import Cart, CartItem, ShopOrder, ShopOrderItem, Coupon, Product


class CartService:
    """Logika biznesowa koszyka zakupowego."""

    @staticmethod
    def get_or_create_cart(user=None, session_key=None):
        """Pobierz lub utwórz koszyk (po użytkowniku lub sesji)."""
        if user and user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart

    @staticmethod
    def add_to_cart(cart: Cart, product_id: int, quantity: int = 1) -> CartItem:
        """Dodaj produkt do koszyka.

        Jeśli produkt już jest w koszyku, zwiększa ilość.
        """
        product = Product.objects.get(pk=product_id, is_active=True)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            # Produkt już w koszyku — zwiększ ilość
            item.quantity += quantity
            item.save()
        return item

    @staticmethod
    def update_quantity(cart: Cart, item_id: int, quantity: int) -> CartItem:
        """Zmień ilość produktu w koszyku.

        Jeśli quantity <= 0, usuwa element. Ogranicza ilość do stanu magazynowego.
        """
        item = CartItem.objects.get(pk=item_id, cart=cart)
        if quantity <= 0:
            item.delete()
            return None
        # Nie pozwól zamówić więcej niż stan magazynowy
        item.quantity = min(quantity, item.product.stock)
        item.save()
        return item

    @staticmethod
    def clear_cart(cart: Cart):
        """Usuń wszystkie elementy z koszyka."""
        cart.items.all().delete()


class CheckoutService:
    """Logika biznesowa zamówień sklepowych."""

    @staticmethod
    def create_order_from_cart(cart: Cart, shipping_data: dict, user) -> ShopOrder:
        """Utwórz zamówienie z koszyka.

        Waliduje stan magazynowy, tworzy zamówienie i jego elementy,
        zmniejsza stock produktów, czyści koszyk.

        Raises:
            ValueError: koszyk pusty lub niewystarczający stan magazynowy
        """
        if not cart.items.exists():
            raise ValueError('Koszyk jest pusty.')

        # Walidacja stanu magazynowego przed utworzeniem zamówienia
        for item in cart.items.select_related('product').all():
            if item.quantity > item.product.stock:
                raise ValueError(f'Niewystarczajacy stan: {item.product.name}')

        order = ShopOrder.objects.create(
            user=user,
            total=cart.total,
            **shipping_data,
        )

        # Tworzenie elementów zamówienia i zmniejszanie stanu magazynowego
        for item in cart.items.select_related('product').all():
            ShopOrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.product.price,
                subtotal=item.subtotal,
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=['stock'])

        # Wyczyść koszyk po złożeniu zamówienia
        CartService.clear_cart(cart)
        return order

    @staticmethod
    def validate_coupon(code: str, order_amount: Decimal) -> dict:
        """Waliduj kupon rabatowy i oblicz kwotę rabatu.

        Sprawdza: aktywność, datę ważności, limit użyć, minimalną kwotę.
        Rabat nie może przekroczyć kwoty zamówienia.

        Returns:
            dict z kluczami: discount (Decimal), coupon (Coupon)
        Raises:
            ValueError: kupon nieprawidłowy, wygasły, wykorzystany lub za niska kwota
        """
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
        except Coupon.DoesNotExist:
            raise ValueError('Nieprawidlowy kupon.')

        now = timezone.now()
        if now < coupon.valid_from or now > coupon.valid_until:
            raise ValueError('Kupon wygasl.')
        if coupon.max_uses > 0 and coupon.times_used >= coupon.max_uses:
            raise ValueError('Kupon zostal juz wykorzystany.')
        if order_amount < coupon.min_order_amount:
            raise ValueError(f'Min. kwota zamowienia: {coupon.min_order_amount} PLN')

        # Oblicz rabat w zależności od typu kuponu
        if coupon.discount_type == 'percentage':
            discount = order_amount * coupon.discount_value / 100
        else:
            discount = coupon.discount_value

        # Rabat nie może przekroczyć kwoty zamówienia
        return {'discount': min(discount, order_amount), 'coupon': coupon}

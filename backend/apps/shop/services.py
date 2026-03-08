from decimal import Decimal
from django.utils import timezone
from .models import Cart, CartItem, ShopOrder, ShopOrderItem, Payment, Coupon, Product


class CartService:
    """Logika biznesowa koszyka."""

    @staticmethod
    def get_or_create_cart(user=None, session_key=None):
        if user and user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart

    @staticmethod
    def add_to_cart(cart: Cart, product_id: int, quantity: int = 1) -> CartItem:
        product = Product.objects.get(pk=product_id, is_active=True)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    @staticmethod
    def update_quantity(cart: Cart, item_id: int, quantity: int) -> CartItem:
        item = CartItem.objects.get(pk=item_id, cart=cart)
        if quantity <= 0:
            item.delete()
            return None
        item.quantity = min(quantity, item.product.stock)
        item.save()
        return item

    @staticmethod
    def clear_cart(cart: Cart):
        cart.items.all().delete()


class CheckoutService:
    """Logika biznesowa zamowien sklepowych."""

    @staticmethod
    def create_order_from_cart(cart: Cart, shipping_data: dict, user) -> ShopOrder:
        if not cart.items.exists():
            raise ValueError('Koszyk jest pusty.')

        # Validate stock
        for item in cart.items.select_related('product').all():
            if item.quantity > item.product.stock:
                raise ValueError(f'Niewystarczajacy stan: {item.product.name}')

        order = ShopOrder.objects.create(
            user=user,
            total=cart.total,
            **shipping_data,
        )

        # Create order items and decrease stock
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

        # Clear cart
        CartService.clear_cart(cart)
        return order

    @staticmethod
    def validate_coupon(code: str, order_amount: Decimal) -> dict:
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

        if coupon.discount_type == 'percentage':
            discount = order_amount * coupon.discount_value / 100
        else:
            discount = coupon.discount_value

        return {'discount': min(discount, order_amount), 'coupon': coupon}

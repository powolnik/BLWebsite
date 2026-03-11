"""
BLACK LIGHT Collective — Shop / Views
Endpointy REST API sklepu: kategorie, produkty, koszyk,
checkout (składanie zamówienia), walidacja kuponów, historia zamówień.
"""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import ProductCategory, Product, ShopOrder
from .serializers import (
    ProductCategorySerializer, ProductListSerializer, ProductDetailSerializer,
    CartSerializer, CartItemSerializer, ShopOrderSerializer,
    CheckoutSerializer, CouponValidateSerializer,
)
from .services import CartService, CheckoutService


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista kategorii produktów (tylko root — parent=None, bez paginacji)."""
    queryset = ProductCategory.objects.filter(parent=None)
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista produktów z filtrami, wyszukiwarką i sortowaniem.

    Lookup po slug. Lista → skrócony serializer, detal → pełny z galerią.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Detal → pełny serializer; lista → skrócony."""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer


class CartView(APIView):
    """Koszyk użytkownika — GET/POST/PUT/DELETE.

    GET: pobierz koszyk
    POST: dodaj produkt
    PUT: zmień ilość
    DELETE: wyczyść koszyk
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Pobierz aktualny stan koszyka użytkownika."""
        cart = CartService.get_or_create_cart(user=request.user)
        return Response(CartSerializer(cart, context={'request': request}).data)

    def post(self, request):
        """Dodaj produkt do koszyka."""
        cart = CartService.get_or_create_cart(user=request.user)
        try:
            item = CartService.add_to_cart(
                cart, request.data.get('product_id'), request.data.get('quantity', 1)
            )
            return Response(
                CartItemSerializer(item, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Zmień ilość produktu w koszyku."""
        cart = CartService.get_or_create_cart(user=request.user)
        item = CartService.update_quantity(
            cart, request.data.get('item_id'), request.data.get('quantity', 1)
        )
        if item is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(CartItemSerializer(item, context={'request': request}).data)

    def delete(self, request):
        """Wyczyść wszystkie elementy koszyka."""
        cart = CartService.get_or_create_cart(user=request.user)
        CartService.clear_cart(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    """Proces składania zamówienia sklepowego.

    1. Walidacja danych wysyłkowych
    2. Utworzenie zamówienia z elementów koszyka
    3. Opcjonalne zastosowanie kuponu rabatowego
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Złóż zamówienie — konwertuje koszyk w zamówienie."""
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = CartService.get_or_create_cart(user=request.user)

        # Wyciągnij dane wysyłkowe z walidowanych danych
        shipping_data = {
            k: data[k] for k in [
                'shipping_name', 'shipping_street', 'shipping_city',
                'shipping_postal_code', 'shipping_country',
            ]
        }
        if data.get('notes'):
            shipping_data['notes'] = data['notes']

        try:
            order = CheckoutService.create_order_from_cart(cart, shipping_data, request.user)

            # Zastosuj kupon jeśli podano
            if data.get('coupon_code'):
                result = CheckoutService.validate_coupon(data['coupon_code'], order.total)
                order.discount = result['discount']
                order.save(update_fields=['discount'])
                result['coupon'].times_used += 1
                result['coupon'].save(update_fields=['times_used'])

            return Response(ShopOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CouponValidateView(APIView):
    """Walidacja kodu kuponu — sprawdza ważność, limity i minimalną kwotę."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Sprawdź kupon i zwróć obliczoną kwotę rabatu."""
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = CartService.get_or_create_cart(user=request.user)
        try:
            result = CheckoutService.validate_coupon(
                serializer.validated_data['code'], cart.total
            )
            return Response({'discount': str(result['discount']), 'valid': True})
        except ValueError as e:
            return Response({'error': str(e), 'valid': False}, status=status.HTTP_400_BAD_REQUEST)


class ShopOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Historia zamówień sklepowych użytkownika (tylko odczyt)."""
    serializer_class = ShopOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Zwraca zamówienia bieżącego użytkownika z elementami."""
        return ShopOrder.objects.filter(user=self.request.user).prefetch_related('items')

from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import ProductCategory, Product, Cart, ShopOrder
from .serializers import (
    ProductCategorySerializer, ProductListSerializer, ProductDetailSerializer,
    CartSerializer, CartItemSerializer, ShopOrderSerializer,
    CheckoutSerializer, CouponValidateSerializer,
)
from .services import CartService, CheckoutService


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.filter(parent=None)
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer


class CartView(APIView):
    """Koszyk uzytkownika."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
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
        """Zmien ilosc produktu w koszyku."""
        cart = CartService.get_or_create_cart(user=request.user)
        item = CartService.update_quantity(
            cart, request.data.get('item_id'), request.data.get('quantity', 1)
        )
        if item is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(CartItemSerializer(item, context={'request': request}).data)

    def delete(self, request):
        """Wyczysc koszyk."""
        cart = CartService.get_or_create_cart(user=request.user)
        CartService.clear_cart(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    """Proces zamawiania."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = CartService.get_or_create_cart(user=request.user)
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

            # Apply coupon if provided
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
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
    """Historia zamowien sklepowych."""
    serializer_class = ShopOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShopOrder.objects.filter(user=self.request.user).prefetch_related('items')

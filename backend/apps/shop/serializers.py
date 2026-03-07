from rest_framework import serializers
from .models import (
    ProductCategory, Product, ProductImage, Cart, CartItem,
    ShopOrder, ShopOrderItem, Payment, Coupon,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products.count', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'product_count', 'children']

    def get_children(self, obj):
        children = obj.children.all()
        return ProductCategorySerializer(children, many=True).data if children else []


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'compare_price', 'category_name', 'primary_image',
            'is_in_stock', 'is_featured',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'compare_price', 'sku', 'stock', 'is_in_stock',
            'is_featured', 'weight_kg', 'tags', 'category', 'images',
            'created_at',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', read_only=True, max_digits=10, decimal_places=2
    )
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_price',
            'product_image', 'quantity', 'subtotal',
        ]

    def get_product_image(self, obj):
        img = obj.product.primary_image
        if img:
            request = self.context.get('request')
            return request.build_absolute_uri(img.url) if request else img.url
        return None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'item_count', 'updated_at']


class ShopOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price', 'subtotal']


class ShopOrderSerializer(serializers.ModelSerializer):
    items = ShopOrderItemSerializer(many=True, read_only=True)
    grand_total = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = ShopOrder
        fields = [
            'id', 'status', 'total', 'shipping_cost', 'discount', 'grand_total',
            'shipping_name', 'shipping_street', 'shipping_city',
            'shipping_postal_code', 'shipping_country', 'tracking_number',
            'notes', 'items', 'created_at',
        ]


class CheckoutSerializer(serializers.Serializer):
    """Serializer do procesu checkout."""
    shipping_name = serializers.CharField(max_length=200)
    shipping_street = serializers.CharField(max_length=300)
    shipping_city = serializers.CharField(max_length=100)
    shipping_postal_code = serializers.CharField(max_length=10)
    shipping_country = serializers.CharField(max_length=100, default='Polska')
    payment_provider = serializers.ChoiceField(choices=['stripe', 'payu', 'p24'])
    coupon_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

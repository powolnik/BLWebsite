from django.contrib import admin
from .models import (
    ProductCategory, Product, ProductImage, Cart, CartItem,
    ShopOrder, ShopOrderItem, Payment, Coupon,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ShopOrderItemInline(admin.TabularInline):
    model = ShopOrderItem
    extra = 0
    readonly_fields = ['unit_price', 'subtotal']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_name']
    inlines = [ShopOrderItemInline]
    date_hierarchy = 'created_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'provider', 'amount', 'status', 'created_at']
    list_filter = ['provider', 'status']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'times_used', 'is_active']
    list_filter = ['discount_type', 'is_active']

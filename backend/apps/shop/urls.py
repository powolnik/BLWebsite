from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.ProductCategoryViewSet, basename='product-category')
router.register('products', views.ProductViewSet, basename='product')
router.register('orders', views.ShopOrderViewSet, basename='shop-order')

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('coupon/validate/', views.CouponValidateView.as_view(), name='coupon-validate'),
    path('', include(router.urls)),
]

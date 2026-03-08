from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('templates', views.SceneTemplateViewSet, basename='template')
router.register('categories', views.ComponentCategoryViewSet, basename='category')
router.register('components', views.ComponentViewSet, basename='component')
router.register('orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

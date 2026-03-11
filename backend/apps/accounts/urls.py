"""
BLACK LIGHT Collective — Accounts / URLs
Routing endpointów kont: rejestracja, profil, CRUD adresów.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('addresses', views.UserAddressViewSet, basename='address')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]

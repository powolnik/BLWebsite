"""
BLACK LIGHT Collective — Accounts / Views
Endpointy REST API do rejestracji, profilu użytkownika
oraz CRUD adresów (z akcją ustawienia domyślnego adresu).
"""
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserAddressSerializer
from .models import UserAddress

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Rejestracja nowego użytkownika (endpoint publiczny)."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Odczyt i aktualizacja profilu zalogowanego użytkownika.

    Nie wymaga podawania PK — obiekt pobierany jest z request.user.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Zwraca bieżącego użytkownika jako obiekt do odczytu/edycji."""
        return self.request.user


class UserAddressViewSet(viewsets.ModelViewSet):
    """CRUD adresów użytkownika.

    Każdy użytkownik widzi i zarządza wyłącznie swoimi adresami.
    Dodatkowa akcja `set_default` ustawia wybrany adres jako domyślny.
    """
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtruje adresy do tych należących do bieżącego użytkownika."""
        return UserAddress.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Ustaw wybrany adres jako domyślny.

        Najpierw resetuje flagę is_default na wszystkich adresach użytkownika,
        a następnie ustawia ją na wybranym adresie.
        """
        address = self.get_object()
        # Reset all addresses, then set this one as default
        UserAddress.objects.filter(user=request.user).update(is_default=False)
        address.is_default = True
        address.save()
        return Response({'status': 'Ustawiono jako domyslny'})

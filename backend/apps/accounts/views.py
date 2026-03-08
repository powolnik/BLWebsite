from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserAddressSerializer
from .models import UserAddress

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Rejestracja nowego uzytkownika."""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Profil zalogowanego uzytkownika."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserAddressViewSet(viewsets.ModelViewSet):
    """CRUD adresow uzytkownika."""
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        address = self.get_object()
        UserAddress.objects.filter(user=request.user).update(is_default=False)
        address.is_default = True
        address.save()
        return Response({'status': 'Ustawiono jako domyslny'})

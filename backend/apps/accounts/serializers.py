"""
BLACK LIGHT Collective — Accounts / Serializers
Serializery do rejestracji, profilu użytkownika oraz adresów.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserAddress

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer rejestracji — waliduje zgodność haseł i tworzy użytkownika."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'company',
        ]

    def validate(self, data):
        """Sprawdza, czy hasło i potwierdzenie są identyczne."""
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Hasla sie nie zgadzaja.'})
        return data

    def create(self, validated_data):
        """Tworzy użytkownika z zahashowanym hasłem (create_user)."""
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer profilu — pola tylko do odczytu: id, username, role, date_joined."""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'avatar', 'bio', 'role', 'company', 'website',
            'date_joined',
        ]
        read_only_fields = ['id', 'username', 'role', 'date_joined']


class UserAddressSerializer(serializers.ModelSerializer):
    """Serializer adresów — automatycznie przypisuje użytkownika z kontekstu żądania."""
    class Meta:
        model = UserAddress
        fields = ['id', 'label', 'street', 'city', 'postal_code', 'country', 'is_default']

    def create(self, validated_data):
        """Przypisuje bieżącego użytkownika do nowego adresu."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

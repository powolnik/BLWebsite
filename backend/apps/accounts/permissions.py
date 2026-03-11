"""
BLACK LIGHT Collective — Accounts / Permissions
Uprawnienia REST API oparte na rolach użytkowników.
Wykorzystywane w widokach konfiguratora, sklepu i portfolio.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Tylko właściciel obiektu może go edytować; reszta — tylko odczyt."""

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, HEAD, OPTIONS — dozwolone dla wszystkich
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsTeamMember(permissions.BasePermission):
    """Dostęp tylko dla członków zespołu (role: member lub admin)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('member', 'admin')


class IsAdminUser(permissions.BasePermission):
    """Dostęp tylko dla administratorów platformy (role: admin)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

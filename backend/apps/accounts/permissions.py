from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Tylko wlasciciel moze edytowac."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsTeamMember(permissions.BasePermission):
    """Dostep tylko dla czlonkow zespolu."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('member', 'admin')


class IsAdminUser(permissions.BasePermission):
    """Dostep tylko dla adminow."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

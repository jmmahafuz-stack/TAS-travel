from rest_framework import permissions


class IsCustomerOrReadOnly(permissions.BasePermission):
    """Allow read-only access to anyone, but non-safe methods only for users with role 'user'."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', '') == 'user'

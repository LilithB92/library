from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """Проверяет, является пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Librarian").exists()

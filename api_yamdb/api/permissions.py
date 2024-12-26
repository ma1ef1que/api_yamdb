from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.is_staff
                 or request.user.is_admin)
        )


class AuthorOrReadOnly(permissions.BasePermission):

    message = "Изменение чужого контента запрещено!"

    def has_object_permission(self, request, view, obj):
        print(f"Request method: {request.method}, "
              f"User: {request.user}, Author: {obj.author}")

        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.author == request.user
            or request.user.is_staff
            or getattr(request.user, 'is_admin', False)
            or getattr(request.user, 'is_moderator', False)
        )


class IsAdmin(permissions.BasePermission):
    """
    Разрешение для администратора или суперпользователя.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin
        return False


class IsModerator(permissions.BasePermission):
    """
    Разрешение для модераторов проекта.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsUser(permissions.BasePermission):
    """
    Разрешение для авторизованных пользователей.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

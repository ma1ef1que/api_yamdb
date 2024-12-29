from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Для аутентифицированных пользователей имеющих статус администратора или
    персонала иначе только просмотр.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.is_staff
                    or request.user.is_admin
                )
            )
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Анонимному пользователю разрешены только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю, админу, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdmin(permissions.BasePermission):
    """
    Разрешение для администратора или суперпользователя.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )

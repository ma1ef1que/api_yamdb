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

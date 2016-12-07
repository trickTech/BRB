from rest_framework import permissions
from brb.utils import error_response


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return error_response({'detail': 'Unauthorised'}, status=401)
        return func(request, *args, **kwargs)

    return wrapper

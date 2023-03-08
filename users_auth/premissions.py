from rest_framework.permissions import BasePermission


class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return True
        if request.method in ['PATCH']:
            if not request.user.is_authenticated:
                return True
            return False



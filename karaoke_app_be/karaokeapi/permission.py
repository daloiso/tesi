from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class OnlyMe(permissions.BasePermission):
    """
    Custom permission to only allow the user with username 'pasquale.daloiso@gmail.com'
    to access or modify the object.
    """
    def has_object_permission(self, request, view, obj):
        # Ensure the user is authenticated and check if the username matches
        if request.user.is_authenticated:
            return request.user.id == 1
        return False

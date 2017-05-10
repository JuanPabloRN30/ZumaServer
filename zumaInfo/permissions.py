from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner.
        if(hasattr(obj, 'user')):
            return obj.user == request.user
        elif (hasattr(obj, 'trabajador')):
            return obj.customer.user == request.user
        elif (hasattr(obj, 'cliente')):
            return obj.customer.user == request.user
        else:
            return False

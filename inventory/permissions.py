from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Admin', 'Manager']

class IsAdminOrChef(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Admin', 'Chef']

class IsChefReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'Chef':
            return request.method in SAFE_METHODS
        return request.user.is_authenticated

class IsManagerReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'Manager':
            return request.method in SAFE_METHODS
        return request.user.is_authenticated
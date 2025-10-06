from rest_framework import generics, permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsCompanyMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        company = None
        if hasattr(obj, "company"):
            company = obj.company
        elif hasattr(obj, "storage"):
            company = obj.storage.company
        elif hasattr(obj, "supplier"):
            company = obj.supplier.company
        return hasattr(user, "owned_company") and user.owned_company == company or getattr(user, "company", None) == company

    

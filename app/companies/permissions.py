from rest_framework import generics, permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsCompanyMember(permissions.BasePermission):
    def has_permission(self, request):
        return request.user

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, "owned_company") and obj.company == user.owned_company:
            return True
        if hasattr(user, "company") and user.company == obj.company:
            return True
        return False
    

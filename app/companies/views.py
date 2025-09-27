from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Company
from .serializers import CompanySerializer

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, "owned_company"):
            raise PermissionDenied("У этого пользователя уже есть компания")
        
        company = serializer.save(owner=user)
        user.is_company_owner = True
        user.company = company
        user.save()


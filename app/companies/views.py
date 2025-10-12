from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models import Company, Storage, Supplier, Supply, Product, Sale
from .serializers import CompanySerializer, StorageSerializer, SupplierSerializer, SupplySerializer, SupplyListSerializer, ProductSerializer, AddUserToCompanySerializer, SaleSerializer, ProductSaleSerializer
from .permissions import IsOwnerOrReadOnly, IsCompanyMember

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class StorageCreateView(generics.CreateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.owned_company)

class StorageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class SupplierListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]
    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.owned_company)

class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.owned_company)    

class SupplyListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "owned_company"):
            return Supply.objects.filter(supplier__company=user.owned_company)
        elif hasattr(user, "company"):
            return Supply.objects.filter(supplier__company=user.company)
        return Supply.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplyListSerializer
        return SupplySerializer

class SupplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owned_company'):
            return Supply.objects.filter(supplier__company=user.owned_company)
        elif hasattr(user, 'company'):
            return Supply.objects.filter(supplier__company=user.company)
        return Supply.objects.none()

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owned_company'):
            return Product.objects.filter(storage__company=user.owned_company)
        elif hasattr(user, 'company'):
            return Product.objects.filter(storage__company=user.company)
        return Product.objects.none()
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owned_company'):
            return Product.objects.filter(storage__company=user.owned_company)
        elif hasattr(user, 'company'):
            return Product.objects.filter(storage__company=user.company)
        return Product.objects.none()

User = get_user_model()
class AddUserToCompanyView(generics.UpdateAPIView):
    serializer_class = AddUserToCompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, "owner_company"):
            return Response({"detail": "Только владелец компании может добавлять пользователей"}, status=status.HTTP_403_FORBIDDEN)
        email = request.data.get("email")
        target_user = User.objects.filter(email=email).first()
        if not target_user:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        target_user.company = user.owned_company
        target_user.save()
        return Response({"detail": f"Пользователь {email} прикреплён к компании {user.owned_company.name}"}, status=status.HTTP_200_OK)
    
class SaleCreateView(generics.ListCreateAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "owned_company"):
            return Sale.objects.filter(company=user.owned_company).order_by("-sale_date")
        return Sale.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, "owned_company") or user.owned_company is None:
            raise PermissionError("Вы не являетесь владельцем компании и не можете создавать продажи.")

        serializer.save(company=user.owned_company)

class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'owned_company'):
            return Sale.objects.filter(company=user.owned_company)
        elif hasattr(user, 'company'):
            return Sale.objects.filter(company=user.company)
        return Sale.objects.none()

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Company, Storage, Supplier, Supply, Product
from .serializers import CompanySerializer, StorageSerializer, SupplierSerializer, SupplySerializer, SupplyListSerializer, ProductSerializer
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
            return Supply.object.filter(supplier__company=user.company)
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



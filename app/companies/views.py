from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Company, Storage, Supplier
from .serializers import CompanySerializer, StorageSerializer, SupplierSerializer
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




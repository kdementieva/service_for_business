from django.urls import path
from .views import CompanyCreateView, CompanyDetailView, StorageCreateView, StorageDetailView, SupplierListCreateView, SupplierDetailView

urlpatterns = [
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    path("storages/", StorageCreateView.as_view(), name="storage-create"),
    path("storage/<int:pk>/", StorageDetailView.as_view(), name="storage-detail"),
    path("suppliers/", SupplierListCreateView.as_view(), name="supplier-list-create"),
    path("suppliers/<int:pk>/", SupplierDetailView.as_view(), name="supplier-detail"),
]
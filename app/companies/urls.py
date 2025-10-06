from django.urls import path
from .views import CompanyCreateView, CompanyDetailView, StorageCreateView, StorageDetailView, SupplierListCreateView, SupplierDetailView, SupplyListCreateView, SupplyDetailView, ProductListCreateView, ProductDetailView, AddUserToCompanyView

urlpatterns = [
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    path("storages/", StorageCreateView.as_view(), name="storage-create"),
    path("storage/<int:pk>/", StorageDetailView.as_view(), name="storage-detail"),
    path("suppliers/", SupplierListCreateView.as_view(), name="supplier-list-create"),
    path("suppliers/<int:pk>/", SupplierDetailView.as_view(), name="supplier-detail"),
    path("supplies/", SupplyListCreateView.as_view(), name="supply-list-create"),
    path("supplies/<int:pk>/", SupplyDetailView.as_view(), name="supply-detail"),
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("companies/add-user/", AddUserToCompanyView.as_view(), name="add-user-to-company"),
]
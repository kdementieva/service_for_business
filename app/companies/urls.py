from django.urls import path
from .views import CompanyCreateView, CompanyDetailView, StorageCreateView, StorageDetailView

urlpatterns = [
    path("create/", CompanyCreateView.as_view(), name="company-create"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
    path("storages/", StorageCreateView.as_view(), name="storage-create"),
    path("storage/<int:pk>/", StorageDetailView.as_view(), name="storage-detail"),
]
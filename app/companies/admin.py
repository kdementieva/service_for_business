from django.contrib import admin
from .models import Company, Storage

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "inn", "owner")   
    search_fields = ("name", "inn")          
    list_filter = ("owner",)                  

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "address")
    search_fields = ("name", "address")
    list_filter = ("company",)

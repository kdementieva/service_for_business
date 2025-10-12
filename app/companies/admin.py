from django.contrib import admin
from .models import Company, Storage, Supplier, Supply, SupplyProduct, Product, Sale, ProductSale

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

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "inn", "company", "email", "phone")
    search_fields = ("name", "inn", "email")
    list_filter = ("company",)

class SupplyProductInline(admin.TabularInline):
    model = SupplyProduct
    extra = 1

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier_id", "delivery_date")
    list_filter = ("supplier_id",) 
    inlines = [SupplyProductInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "storage_id", "quantity", "purchase_price", "sale_price")
    search_fields = ("name",)
    list_filter = ("storage_id",)

class ProductSaleInline(admin.TabularInline):
    model = ProductSale
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("buyer_name", "sale_date", "company")
    search_fields = ("company__name", "buyer_name")
    list_filter = ("sale_date",)
    inlines = [ProductSaleInline]



from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, unique=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_company")
    def __str__(self):
        return f"{self.name} ({self.inn})"


class Storage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="storages")
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.name} ({self.company.name})"
    
class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="suppliers")
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.inn} - {self.company.name})"

class Product(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name="products", null=False, blank=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.name} ({self.quantity} шт., склад: {self.storage.name})"
    
class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplies", null=False, blank=False)
    delivery_date = models.DateField()
    products = models.ManyToManyField(Product, through="SupplyProduct", related_name="supplies")
    def __str__(self):
        return f"Поставка #{self.id} от {self.delivery_date} ({self.supplier.name})"
    
class SupplyProduct(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name="supply_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_supplies")
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.product.name} — {self.quantity} шт. (Поставка {self.supply.id})"
    
class Sale(models.Model):
    buyer_name = models.CharField(max_length=255)
    sale_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_sales", null=False, blank=False)
    products_sales = models.ManyToManyField(Product, through="ProductSale", related_name="sales")
    def __str__(self):
        return f"Продажа #{self.id} от {self.sale_date} ({self.company.name})"
    
class ProductSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="product_links")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_sales")
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт. (Продажа {self.sale.id})"


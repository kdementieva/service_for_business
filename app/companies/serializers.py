from rest_framework import serializers
from .models import Company, Storage, Supplier, Supply, SupplyProduct, Product, Sale, ProductSale

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'inn']

    def validate_inn(self, value):
        if not value.isdigit() or len(value) not in (10, 12):
            raise serializers.ValidationError("ИНН должен содержать 10 или 12 цифр")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'owned_company'):
            raise serializers.ValidationError("У вас уже есть компания")
        validated_data['owner'] = user
        return super().create(validated_data)

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'name', 'address', 'company']
        read_only_fields = ['company']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'inn', 'phone', 'email', 'company']
        read_only_fields = ['company']

    def validate_inn(self, value):
        if not value.isdigit() or len(value) not in (10, 12):
            raise serializers.ValidationError("ИНН должен содержать 10 или 12 цифр")
        return value  
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['company'] = user.owned_company
        return super().create(validated_data)

class SupplyProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = SupplyProduct
        fields = ['product', 'product_name', 'quantity']

class SupplySerializer(serializers.ModelSerializer):
    supply_items = SupplyProductSerializer(many=True, write_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(source='supplier', queryset=Supplier.objects.all(), write_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    delivery_date = serializers.DateField()
    class Meta:
        model = Supply
        fields = ['id', 'supplier_id', 'supplier_name', 'delivery_date', 'supply_items']
    
    def create(self, validated_data):
        supply_items_data = validated_data.pop('supply_items')
        supply = Supply.objects.create(**validated_data)

        for item_data in supply_items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if quantity <= 0:
                raise serializers.ValidationError("Количество должно быть положительным числом")
            
            SupplyProduct.objects.create(supply=supply, product=product, quantity=quantity)
            product.quantity += quantity
            product.save()
        return supply

class ProductSerializer(serializers.ModelSerializer):
    storage_id = serializers.PrimaryKeyRelatedField(source='storage', queryset=Storage.objects.all(), write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'purchase_price', 'sale_price', 'quantity', 'storage_id']
        read_only_fields = ['quantity']

    def create(self, validated_data):
        validated_data['quantity'] = 0
        return super().create(validated_data)

class SupplyListSerializer(serializers.ModelSerializer):
    products = SupplyProductSerializer(source='supply_items', many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    class Meta:
        model = Supply
        fields = ['id', 'supplier_name', 'delivery_date', 'products']

class AddUserToCompanySerializer(serializers.Serializer):
    email = serializers.EmailField()

class ProductSaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = ProductSale
        fields = ['product', 'product_name', 'quantity']


class SaleSerializer(serializers.ModelSerializer):
    products_sales = ProductSaleSerializer(source='product_links', many=True)

    class Meta:
        model = Sale
        fields = ['id', 'buyer_name', 'sale_date', 'company', 'products_sales']
        read_only_fields = ['company']

    def create(self, validated_data):
        products_data = validated_data.pop('product_links')
        user = self.context['request'].user
        validated_data['company'] = user.owned_company
        sale = Sale.objects.create(**validated_data)

        for item in products_data:
            product = item['product']
            quantity = item['quantity']

            if quantity <= 0:
                raise serializers.ValidationError("Количество должно быть положительным числом")
            if product.quantity < quantity:
                raise serializers.ValidationError(f"Недостаточно товара: {product.name}")

            ProductSale.objects.create(sale=sale, product=product, quantity=quantity)
            product.quantity -= quantity
            product.save()

        return sale

    def update(self, instance, validated_data):
        validated_data.pop('product_links', None)
        return super().update(instance, validated_data)

from rest_framework import serializers
from .models import Company, Storage

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
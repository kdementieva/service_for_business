from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'inn']

    def validate_inn(self, value):
        if not value.isdigit() or len(value) not in (10, 12):
            raise serializers.ValidationError("ИНН должен содержать 10 или 12 цифр")
        return value
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
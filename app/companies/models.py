from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, unique=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_company")
    # storage = models.OneToOneField("companies.Storage", null=True, blank=True, on_delete=models.SET_NULL, related_name="company")
    def __str__(self):
        return f"{self.name} ({self.inn})"

from django.db import models
from accounts.models import Address

class Workshop(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    
    def __str__(self):
        return f"{self.name} at {self.workshop.name}"
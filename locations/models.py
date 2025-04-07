from django.db import models
from django.forms import ValidationError

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name_plural = "Addresses"
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

    def clean(self):
        # Validate coordinates
        if not (-90 <= self.latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90")
        if not (-180 <= self.longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180")
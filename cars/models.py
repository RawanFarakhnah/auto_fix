import datetime
from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class CarManager(models.Manager):
    def car_validator(self, postData, instance=None):
        errors = {}

        # Validate make
        if not postData['make'] or not postData['make'].strip():
            errors['make'] = "Make cannot be empty."

        # Validate model
        if not postData['model'] or not postData['model'].strip():
            errors['model'] = "Model cannot be empty."

        # Validate year
        current_year = datetime.datetime.now().year
        if postData['year'] is not None:
            if int(postData['year']) < 1886 or int(postData['year']) > current_year:
                errors['year'] = f"The year must be between 1886 and {current_year}."

        # Validate VIN
        vin = postData.get('vin', '').strip()
        if vin:
            if len(vin) != 17:
                errors['vin'] = "VIN must be exactly 17 characters long."
            elif not vin.isalnum():
                errors['vin'] = "VIN must contain only letters and numbers."
            else:
                # Check if VIN exists, excluding current instance if editing
                qs = Car.objects.filter(vin=vin)
                if instance:
                    qs = qs.exclude(id=instance.id)
                if qs.exists():
                    errors['vin'] = "A car with this VIN already exists."
        else:
            errors['vin'] = "VIN is required."
        
        return errors


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    vin = models.CharField(max_length=17, unique=True)
    objects = CarManager()

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
from django.db import models
from accounts.models import User

# Create your models here.
class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    vin = models.CharField(max_length=17, unique=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
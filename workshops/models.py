from django.db import models
from accounts.models import Address, User

class WorkshopManager(models.Manager):
    def validation(self,data):
        errors= {}
        if len(data['name']) < 5 or not data['name'].isalpha():
            errors['name'] ='The name of the workshop must be more than five characters , and must contian only characters!'
        if not data['description']:
            errors['description'] = 'You should fill the discription of your workshop !'
        if not data['phone']:
            errors['phone'] = ' You should insert phone number !'
        if not data['image']:
            errors['image'] = 'Please upload image related to your work shop !'
        return errors
class serviceManager(models.Manager):
    def validation(self,data):
        errors = {}
        if not data['name']:
            errors['name'] = 'You should insert avalid name for your service !'
        if not data['price']:
            errors['price'] = 'You should insert a valid phone number for your service'
        if not data['description']:
            errors['description'] = 'You sould descripe your service !'
        if not data['duration']:
            errors['duration'] = 'You sould insert the time of your service !'
        return errors
    
    
class Workshop(models.Model):
    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='workshops_images/', null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="workshop", null=True)
    objects = WorkshopManager()
    def __str__(self):
        return self.name

class Service(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    objects = serviceManager()
    
    def __str__(self):
        return f"{self.name} at {self.workshop.name}"
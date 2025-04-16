from django.db import models
from django.contrib.auth.models import AbstractUser
from locations.models import Address
import re


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"

        EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email address"
    
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        
        # if postData.get('phone') and not re.match(r'^\d{3}-\d{3}-\d{4}$', postData['phone']):
        #     errors['phone'] =  "enter a valid phone number. Example format: 05xxxxxxxx"
       
        phone = postData.get('phone')
        if not phone or not phone.isdigit():
            errors['phone'] = "Phone number must contain only digits!"
        if not phone or len(phone) != 10:
            errors['phone'] = "Phone number must be 10 digits!"
        if not str(phone).startswith("05"):
             errors['phone'] = "Phone number must start with 05"

        return errors

    def get_by_natural_key(self, email):
        """Override to use email as the unique identifier."""
        return self.get(email=email)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password and other fields.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Normalize the email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def normalize_email(self, email):
        """
        Normalize the email by lowercasing it.
        """
        email = email.strip().lower()
        return email

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True)
    is_workshop_owner = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    objects = UserManager()
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # names required for registration
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
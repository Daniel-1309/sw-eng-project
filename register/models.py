from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    USER_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('restaurant manager', 'Restaurant Manager'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password in practice
    address = models.TextField()
    phone_number = models.CharField(max_length=15)  # Adjust length if necessary
    role = models.CharField(max_length=25, choices=USER_ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    # Linking to the built-in User model with a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields to store user information
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), 
                                                   ('restaurant_manager', 'Restaurant Manager'), 
                                                   ('customer', 'Customer')], 
                            default='customer')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), 
                                                   ('restaurant_manager', 'Restaurant Manager'), 
                                                   ('customer', 'Customer')],
                            default='customer')

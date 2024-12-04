from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('restaurant_manager', 'Restaurant Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"

class MenuItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Orders(models.Model):
    PAYMENT_CHOICES = [
        ('cash_on_delivery', 'Cash On delivery'),
        ('visa', 'Visa')
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash_on_delivery')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    placement_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %Y %I:%M %p")}'
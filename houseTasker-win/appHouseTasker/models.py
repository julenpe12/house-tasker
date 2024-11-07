from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username
    

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('cleaning', 'Limpieza'),
        ('vehicle', 'Vehículo'),
        ('kitchen', 'Cocina'),
        ('others', 'Otros'),
    ]

    name = models.CharField(max_length=100, unique=True, help_text="Nombre del recurso, e.g., Jabon, Coche, Llaves.")
    description = models.TextField(blank=True, help_text="Descripción opcional del recurso y sus características.")
    quantity = models.PositiveIntegerField(default=1, help_text="Cantidad disponible de este recurso.")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='others', help_text="Categoría del recurso.")
    is_available = models.BooleanField(default=True, help_text="Indica si el recurso está disponible para uso.")

    def __str__(self):
        return f"{self.name} ({self.quantity} disponibles)"

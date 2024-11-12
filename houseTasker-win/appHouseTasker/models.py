from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

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

User = get_user_model()

class Task(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=MEDIUM)
    due_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task', null=True)

    def __str__(self):
        return f"{self.title} ({self.due_date})"

    class Meta:
        ordering = ['-due_date', 'priority']
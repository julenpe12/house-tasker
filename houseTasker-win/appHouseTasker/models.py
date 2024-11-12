from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile-pictures/', blank=True, null=True)

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
    start_date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()
    completed = models.BooleanField(default=False)
    resources = models.ManyToManyField('Resource', related_name="tasks", blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def end_date(self):
        return self.start_date + self.duration

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date()})"
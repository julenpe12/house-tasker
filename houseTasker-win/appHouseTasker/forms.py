from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, Task, Resource

class CustomUserCreationForm(UserCreationForm): 
    class Meta(UserCreationForm): 
        model = CustomUser 
        fields = ("username", "email", "profile_image")

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("username", "email", "profile_image")

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'quantity', 'category', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el Recurso...'}),
            'name': forms.TextInput(attrs={'placeholder': 'E.g., Jabón, Coche'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

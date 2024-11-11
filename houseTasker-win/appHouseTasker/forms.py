from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from .models import Resource

class CustomUserCreationForm(UserCreationForm): 
    class Meta(UserCreationForm): 
        model = CustomUser 
        fields = UserCreationForm.Meta.fields + ("profile_image","role",)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("username", "email", "profile_image", "role")

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'quantity', 'category', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el Recurso...'}),
            'name': forms.TextInput(attrs={'placeholder': 'E.g., Jabón, Coche'}),
        }

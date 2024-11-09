from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm): 
    class Meta(UserCreationForm): 
        model = CustomUser 
        fields = UserCreationForm.Meta.fields + ("profile_image","role",)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("username", "email", "profile_image", "role")
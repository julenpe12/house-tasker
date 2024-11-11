from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Task, Resource

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("profile_image", "role",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Resource)
admin.site.register(Task)
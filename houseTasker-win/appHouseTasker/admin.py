from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Task, Resource

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("profile_image",)}),
    )

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'is_available')
    readonly_fields = ('tasks_list',)

    def tasks_list(self, obj):
        return ", ".join([task.title for task in obj.tasks.all()])  # Muestra títulos de tareas
    tasks_list.short_description = "Tareas Asociadas"

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Task)
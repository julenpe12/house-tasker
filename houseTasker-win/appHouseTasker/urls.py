# taskhandler/urls.py

from django.urls import path
from . import views
from .views import CustomLoginView, RegisterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page for task handling
    path('tasks/', views.task_list, name='task_list'),  # List all tasks
    path('tasks/create/', views.task_create, name='task_create'),  # Create a new task
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),  # View task details
    path('tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),  # Edit a task
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),  # Delete a task

    path('resources/', views.resource_list, name='resource_list'),  # List all resources
    path('resources/create/', views.resource_create, name='resource_create'),  # Create a new resources
    path('resources/<int:resource_id>/', views.resource_detail, name='resource_detail'),  # View resources details
    path('resources/<int:resource_id>/edit/', views.resource_edit, name='resource_edit'),  # Edit a resources
    path('resources/<int:resource_id>/delete/', views.resource_delete, name='resource_delete'),  # Delete a resources
    
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
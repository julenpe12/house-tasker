from django.urls import path
from .views import (
    FAQView, HomeView, TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView,
    ResourceListView, ResourceCreateView, ResourceDetailView, ResourceUpdateView, ResourceDeleteView,
    CustomLoginView, RegisterView
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Home page for task handling
    path('faq/', FAQView.as_view(), name='faq'),  # FAQ page
    
    # Task-related URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),  # List all tasks
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),  # Create a new task
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),  # View task details
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),  # Edit a task
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),  # Delete a task
    
    # Resource-related URLs
    path('resources/', ResourceListView.as_view(), name='resource_list'),  # List all resources
    path('resources/create/', ResourceCreateView.as_view(), name='resource_create'),  # Create a new resource
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),  # View resource details
    path('resources/<int:pk>/edit/', ResourceUpdateView.as_view(), name='resource_edit'),  # Edit a resource
    path('resources/<int:pk>/delete/', ResourceDeleteView.as_view(), name='resource_delete'),  # Delete a resource
    
    # Authentication URLs
    path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('accounts/register/', RegisterView.as_view(), name='register'),  # Registration page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    
    # Static files in DEBUG mode
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
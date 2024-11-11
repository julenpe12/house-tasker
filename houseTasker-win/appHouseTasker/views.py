from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ResourceForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from .models import Resource

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def task_list(request):
    return HttpResponse("Here is a list of tasks")

@login_required
def task_create(request):
    return HttpResponse("Create a new task")

@login_required
def task_detail(request, task_id):
    return HttpResponse(f"Viewing task {task_id}")

@login_required
def task_edit(request, task_id):
    return HttpResponse(f"Edit task {task_id}")

@login_required
def task_delete(request, task_id):
    return HttpResponse(f"Delete task {task_id}")

@login_required
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'resource_list.html', {'resources': resources})

@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()

    return render(request, 'resource_create.html', {'form': form})

@login_required
def resource_detail(request, resource_id):
    return HttpResponse(f"Viewing resource {resource_id}")

@login_required
def resource_edit(request, resource_id):
    return HttpResponse(f"Edit resource {resource_id}")

@login_required
def resource_delete(request, resource_id):
    return HttpResponse(f"Delete resource {resource_id}")

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Make sure to create this template
    redirect_authenticated_user = True
    
class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after registration
            return redirect(reverse_lazy('home'))  # Redirect to the homepage or another page
        return render(request, self.template_name, {'form': form})

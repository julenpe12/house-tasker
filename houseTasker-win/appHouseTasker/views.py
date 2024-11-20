from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Task, Resource
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import TaskForm
from .forms import CustomUserCreationForm, ResourceForm
from django.shortcuts import render, redirect
from django.contrib.auth import login


class FAQView(TemplateView):
    template_name = "FAQ.html"


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.filter(completed=False).order_by('start_date').first()
        context['closest_task'] = [task] if task else []
        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = super().get_queryset()
        for task in tasks:
            overlapping = False
            task_end_date = task.start_date + task.duration
            for resource in task.resources.all():
                overlapping_count = sum(
                    1 for t in resource.tasks.exclude(id=task.id)
                    if not (t.start_date >= task_end_date or t.start_date + t.duration <= task.start_date)
                )
                if overlapping_count >= resource.quantity:
                    overlapping = True
                    break

            task.is_overlapping = overlapping
            task.save()
        return tasks


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_create.html"
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.created_by = self.request.user
        start_date = form.cleaned_data['start_date']
        duration = form.cleaned_data['duration']
        end_date = start_date + duration
        resources = form.cleaned_data['resources']

        for resource in resources:
            overlapping_tasks = 0
            for resource_task in resource.tasks.all():
                if not (resource_task.start_date >= end_date or resource_task.start_date + resource_task.duration <= start_date):
                    overlapping_tasks += 1
            if overlapping_tasks >= resource.quantity:
                messages.error(self.request, f"El recurso '{resource.name}' no está disponible.")
                return self.form_invalid(form)

        task.save()
        form.save_m2m()
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_edit.html"
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        task = form.save(commit=False)
        start_date = form.cleaned_data['start_date']
        duration = form.cleaned_data['duration']
        end_date = start_date + duration
        resources = form.cleaned_data['resources']

        for resource in resources:
            overlapping_tasks = 0
            for resource_task in resource.tasks.exclude(id=task.id):
                if not (resource_task.start_date >= end_date or resource_task.start_date + resource_task.duration <= start_date):
                    overlapping_tasks += 1
            if overlapping_tasks >= resource.quantity:
                messages.error(self.request, f"El recurso '{resource.name}' no está disponible.")
                return self.form_invalid(form)

        task.save()
        form.save_m2m()
        messages.success(self.request, "La tarea ha sido actualizada exitosamente.")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy('task_list')


class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    template_name = "resource_list.html"
    context_object_name = "resources"


class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = "resource_create.html"
    success_url = reverse_lazy('resource_list')


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = "resource_detail.html"
    context_object_name = "resource"


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = "resource_edit.html"
    success_url = reverse_lazy('resource_list')

    def form_valid(self, form):
        resource = form.save()
        new_quantity = form.cleaned_data['quantity']
        for task in resource.tasks.all():
            task_end_date = task.start_date + task.duration
            overlapping_count = sum(
                1 for t in resource.tasks.all()
                if not (t.start_date >= task_end_date or t.start_date + t.duration <= task.start_date)
            )
            task.is_overlapping = overlapping_count > new_quantity
            task.save()
        messages.success(self.request, f"Recurso '{resource.name}' actualizado exitosamente.")
        return super().form_valid(form)


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = "resource_delete.html"
    success_url = reverse_lazy('resource_list')
    
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
        form = self.form_class(request.POST, request.FILES)  # Add request.FILES here to handle files
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('home'))
        return render(request, self.template_name, {'form': form})
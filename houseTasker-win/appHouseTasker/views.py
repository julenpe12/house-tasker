from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ResourceForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View
from .models import Resource, Task
from .forms import TaskForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            
            # Obtén la información de fechas del formulario
            start_date = form.cleaned_data['start_date']
            duration = form.cleaned_data['duration']
            print(f"Fecha de inicio: {start_date}")
            print(f"Duración: {duration}")
            
            # Calcula la fecha de finalización
            end_date = start_date + duration
            print(f"Fecha de fin: {end_date}")
            
            # Obtiene los recursos
            resources = form.cleaned_data['resources']
            for resource in resources:
                print(f"Verificando recurso: {resource.name}")
                overlapping_tasks = 0
                for resource_task in resource.tasks.all():
                    print(f" - Comprobando tarea: {resource_task.title}")
                    # Comprueba si hay solapamiento en las fechas
                    if not (resource_task.start_date >= end_date or resource_task.start_date + resource_task.duration <= start_date):
                        overlapping_tasks += 1
                
                # Verifica si el recurso está disponible
                if overlapping_tasks >= resource.quantity:
                    print(f" - Recurso '{resource.name}' no está disponible en el horario especificado.")
                    messages.error(request, f"El recurso '{resource.name}' no está disponible en las horas seleccionadas.")
                    return render(request, 'task_create.html', {'form': form})
            
            # Guarda la tarea si todos los recursos están disponibles
            task.save()
            form.save_m2m()  # Guarda la relación ManyToMany
            print(" - Tarea guardada exitosamente.")
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_create.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_edit(request, task_id):
    # Obtener la tarea o mostrar 404 si no existe
    task = get_object_or_404(Task, id=task_id)

    # Si se envía el formulario con datos, se procesa el formulario
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # Extraer los datos de la tarea y recursos
            start_date = form.cleaned_data['start_date']
            duration = form.cleaned_data['duration']
            end_date = start_date + duration
            resources = form.cleaned_data['resources']

            # Validación para evitar solapamientos de recursos
            for resource in resources:
                overlapping_tasks = 0  # Contador para verificar solapamientos
                for resource_task in resource.tasks.exclude(id=task.id):  # Excluye la tarea actual
                    # Comprobamos solapamientos de fecha entre la tarea editada y otras tareas asignadas al recurso
                    if not (resource_task.start_date >= end_date or resource_task.start_date + resource_task.duration <= start_date):
                        overlapping_tasks += 1

                # Verificar si el recurso está disponible en el horario solicitado
                if overlapping_tasks >= resource.quantity:
                    messages.error(request, f"El recurso '{resource.name}' no está disponible en el horario especificado.")
                    return render(request, 'task_edit.html', {'form': form, 'task': task})
            
            # Si no hay solapamientos, guarda la tarea actualizada
            task = form.save(commit=False)
            task.save()
            form.save_m2m()  # Guarda la relación ManyToMany
            messages.success(request, "La tarea ha sido actualizada exitosamente.")
            return redirect('task_list')  # Redirigir a la lista de tareas después de editar
    else:
        form = TaskForm(instance=task)  # Formulario con los datos de la tarea actual

    return render(request, 'task_edit.html', {'form': form, 'task': task})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_delete.html', {'task': task})

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
    resource = get_object_or_404(Resource, pk=resource_id)
    return render(request, 'resource_detail.html', {'resource': resource})

@login_required
def resource_edit(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)

    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('resource_list')
    else:
        form = ResourceForm(instance=resource)

    return render(request, 'resource_edit.html', {'form': form, 'resource': resource})


@login_required
def resource_delete(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    if request.method == 'POST':
        resource.delete()
        return redirect('resource_list')
    return render(request, 'resource_delete.html', {'resource': resource})

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

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the House Task Handler Home Page")

def task_list(request):
    return HttpResponse("Here is a list of tasks")

def task_create(request):
    return HttpResponse("Create a new task")

def task_detail(request, task_id):
    return HttpResponse(f"Viewing task {task_id}")

def task_edit(request, task_id):
    return HttpResponse(f"Edit task {task_id}")

def task_delete(request, task_id):
    return HttpResponse(f"Delete task {task_id}")

def resource_list(request):
    return HttpResponse("Here is a list of resources")

def resource_create(request):
    return HttpResponse("Create a new resource")

def resource_detail(request, resource_id):
    return HttpResponse(f"Viewing resource {resource_id}")

def resource_edit(request, resource_id):
    return HttpResponse(f"Edit resource {resource_id}")

def resource_delete(request, resource_id):
    return HttpResponse(f"Delete resource {resource_id}")

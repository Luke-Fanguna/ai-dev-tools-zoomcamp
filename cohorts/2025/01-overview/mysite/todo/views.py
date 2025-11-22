from django.shortcuts import render
from .models import Task


def home(request):
    # Query tasks and pass them to the template so tests can see titles
    tasks = Task.objects.all()
    return render(request, "todo/home.html", {"tasks": tasks})

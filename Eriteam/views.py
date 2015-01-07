from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from gantt.models import Project


@login_required
def home(request):
    return render(request, 'Eriteam/home.html', {'projects':Project.objects.all()})

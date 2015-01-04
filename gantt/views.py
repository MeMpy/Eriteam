from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from gantt.models import Project

from gantt.serializers import TaskSerializer, ProjectSerializer


class TaskList(APIView):
    """
    All the project's tasks.

    """

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        serializer = ProjectSerializer(project)

        return Response(serializer.data)
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

#TODO Implements
# class TaskDetail(APIView):
#     """
#     Create, Update or delete a task instance.
#     """
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def get_task(self, project_id,task_id):
#         try:
#             project = get_object_or_404(Project, pk=project_id)
#             return project.task_set.get(id=task_id)
#         except Task.DoesNotExist:
#             raise Http404
#
#     def post(self, request, project_id, format=None):
#
#         task_parent = self.get_task(project_id=project_id, task_id=request.data['parent'])
#         serializer = TaskSerializerRob(data=deserialize(request.data['task']))
#         if serializer.is_valid():
#             serializer.save(parent=task_parent)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, project_id, format=None):
#         task = self.get_task(project_id, request.data['id'])
#         serializer = TaskSerializerRob(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, project_id, format=None):
#         task = self.get_task(project_id, request.data['id'])
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
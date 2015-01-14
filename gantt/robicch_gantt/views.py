from django.http.response import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.six import BytesIO
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from gantt.models import Project, Task
from gantt.robicch_gantt.serializers import ProjectSerializerRob, TaskSerializerRob


def deserialize(content):

    stream = BytesIO(content)
    return JSONParser().parse(stream)





class TaskListRob(APIView):
    """
    All the project's tasks.

    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        try:
            serializer = ProjectSerializerRob(project)
            extra_info = {
                "canWrite":True,
                "canWriteOnParent":True,
                "selectedRow":0,
                "deletedTaskIds":[]
            }

            extra_info.update(serializer.data)

            resp = {'ok': True, 'project': extra_info}

            return Response(resp)

        except Exception:

            return Response({'ok' : False, 'project': None})

    def put(self, request, project_id, format=None):

        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializerRob(project, data=deserialize(request.data['project']))

        if serializer.is_valid():
            serializer.save(user=request.user)

            extra_info = {
                "canWrite":True,
                "canWriteOnParent":True,
                "selectedRow":0,
                "deletedTaskIds":[]
            }

            extra_info.update(serializer.data)

            resp = {'ok': True, 'project': extra_info}

            return Response(resp)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailRob(APIView):
    """
    Create, Update or delete a task instance.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_task(self, project_id,task_id):
        try:
            project = get_object_or_404(Project, pk=project_id)
            return project.task_set.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404

    def post(self, request, project_id, format=None):

        task_parent = self.get_task(project_id=project_id, task_id=request.data['parent'])
        serializer = TaskSerializerRob(data=deserialize(request.data['task']))
        if serializer.is_valid():
            serializer.save(parent=task_parent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id, format=None):
        task = self.get_task(project_id, request.data['id'])
        serializer = TaskSerializerRob(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, format=None):
        task = self.get_task(project_id, request.data['id'])
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def robicch_gantt(request, project_id):

    return render(request, 'gantt/robicch_gantt.html', {'project_id': project_id})
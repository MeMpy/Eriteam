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


def robicch_gantt(request, project_id):

    return render(request, 'gantt/robicch_gantt.html', {'project_id': project_id})
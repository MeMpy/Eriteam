from rest_framework import serializers
from gantt.models import Task, Project, Assignment, Resource


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        exclude = ('task',)


class TaskSerializer(serializers.ModelSerializer):

    assignment_set = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        exclude = ('assigned_to','project')

class ResourceSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='user.username')

    class Meta:
        model = Resource
        exclude=('user',)

    def create(self, validated_data):
        pass


class ProjectSerializer(serializers.ModelSerializer):

    tasks = TaskSerializer(source='task_set', many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('tasks', 'resources')


from rest_framework import serializers
from gantt.models import Task
from gantt.robicch_gantt import helpers
from gantt.serializers import AssignmentSerializer, TaskSerializer, ResourceSerializer, ProjectSerializer


class AssignmentSerializerRob(AssignmentSerializer):

    resourceId = serializers.IntegerField(source='resource.id')

    class Meta(AssignmentSerializer.Meta):
        exclude = AssignmentSerializer.Meta.exclude + ('resource',)


class TaskSerializerRob(TaskSerializer):

    start = serializers.IntegerField(source='start_time_in_millis')
    end = serializers.IntegerField(source='end_time_in_millis')
    depends = serializers.SerializerMethodField('get_dependencies')
    assigs = AssignmentSerializerRob(source='assignment_set', many=True, read_only=True)
    #extra information needed client side. They are all calculated field based on various information
    #TODO calculate!
    # canWrite = serializers.SerializerMethodField()
    # collapsed = serializers.SerializerMethodField()
    # endIsMilestone = serializers.SerializerMethodField()
    # startIsMilestone = serializers.SerializerMethodField()
    hasChild = serializers.SerializerMethodField(method_name='has_child')

    class Meta(TaskSerializer.Meta):
        exclude = TaskSerializer.Meta.exclude + ('start_time','end_time','depends_on', 'parent')

    def __init__(self, *args, **kwargs):

        # Instantiate the superclass normally
        super(TaskSerializerRob, self).__init__(*args, **kwargs)
        #TODO generalize in a common superclass??
        self.fields.pop('assignment_set')

    def has_child(self, obj):
        return  bool(obj.grafted_task_set.count())

    def get_dependencies(self, obj):

        if not obj.depends_on:
            return ""

        dep_str = []
        for d in obj.dependency_set.all():
            if d.delay:
                dep_str.append("{}:{}".format(d.finish_task.row_index, d.delay))
            else:
                dep_str.append(repr(d.finish_task.row_index))
        return  ",".join(dep_str)


class ProjectSerializerRob(ProjectSerializer):

    tasks = TaskSerializerRob(source='task_set', many=True, read_only=True)

    ##############################################
    # ACTIONS
    ##############################################

    def update(self, instance, validated_data):

        user = validated_data.pop('user')

        tasks = self.initial_data['tasks']

        for i in range(len(tasks)):
            helpers.save_task(instance, tasks[i],i,tasks)

        for i in range(len(tasks)):
            helpers.save_dependencies(instance, tasks[i], tasks)

        for i in range(len(tasks)):
            helpers.save_assignments(instance, tasks[i])

        return instance


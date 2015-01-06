from rest_framework import serializers
from gantt.models import Task
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

    ##############################################
    # ACTIONS
    ##############################################

    def create(self, validated_data):
        parent = validated_data.pop('parent')

        assert isinstance(parent, Task)
        return parent.addTask(
                validated_data['name'],
                validated_data['code'],
                validated_data['description'],
                validated_data['row_index'],
                validated_data['start_time_in_millis'],
                validated_data['end_time_in_millis'],
                validated_data['status'],
                validated_data['progress']
                )


class ProjectSerializerRob(ProjectSerializer):

    tasks = TaskSerializerRob(source='task_set', many=True, read_only=True)

    ##############################################
    # ACTIONS
    ##############################################

    def create(self, validated_data):
        user = validated_data.pop('user')


        # return parent.addTask(
        #         validated_data['name'],
        #         validated_data['code'],
        #         validated_data['description'],
        #         validated_data['row_index'],
        #         validated_data['start_time_in_millis'],
        #         validated_data['end_time_in_millis'],
        #         validated_data['status'],
        #         validated_data['progress']
        #         )


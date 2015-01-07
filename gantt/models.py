import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def calcDurationInDays(end_time, start_time):
    return (end_time - start_time).days

def calcTimeInMillis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt.replace(tzinfo=None) - epoch
    return int(delta.total_seconds() * 1000)

def calcDateFromMillis(ms):
    return datetime.datetime.fromtimestamp(ms/1000.0)


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=150)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    duration = models.FloatField()  # calculated each time you save the instance

    resources = models.ManyToManyField('Resource', related_name='work_on')

    @property
    def root_task(self):
        return self.task_set.get(parent__isnull=True)

    def __unicode__(self):
        return u"{name}: start: {start}, end: {end}".format(name=self.name,
                                                           start=self.start_time,
                                                           end=self.end_time)

    def save(self, **kwargs):
        self.duration = calcDurationInDays(self.end_time, self.start_time)

        super(Project, self).save(**kwargs)


class Task(models.Model):

    class Meta:
        ordering = ['row_index']


    STATUS_CHOICES = (
        ("STATUS_ACTIVE", "STATUS_ACTIVE"),
        ("STATUS_DONE", "STATUS_DONE"),
        ("STATUS_FAILED", "STATUS_FAILED"),
        ("STATUS_SUSPENDED", "STATUS_SUSPENDED"),
        ("STATUS_UNDEFINED", "STATUS_UNDEFINED")
    )
    DEFAULT_STATUS = ("STATUS_ACTIVE", "STATUS_ACTIVE")

    name = models.CharField(max_length=150)

    code = models.CharField(max_length=150, blank=True, default="") #TODO it is ok?



    description = models.TextField(max_length=255, default="", blank=True)


    # This is the row in which the task should appear. This can be considered the task's appearance order.
    # This must be unique within the project.task_set. @see clean
    row_index = models.IntegerField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    duration = models.FloatField()

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=DEFAULT_STATUS)

    progress = models.IntegerField(default=0)  # a number that specifies progress: 0%  none 50% half way and so on

    ##############################################
    # CONVERSION
    ##############################################


    def _set_start_time(self, start_time):

        if isinstance(start_time, datetime.datetime):
            self.start_time = start_time
        elif isinstance(start_time, ( int, long )):
            self.start_time = calcDateFromMillis(start_time)

    def _set_end_time(self, end_time):

        if isinstance(end_time, datetime.datetime):
            self.end_time = end_time
        elif isinstance(end_time, int):
            self.end_time = calcDateFromMillis(end_time)

    def set_duration(self, start_time, duration=None, end_time=None):
        """

        :param start_time:
        :param end_time:
        :param duration:
        :return:
        """
        if not end_time and not duration:
            raise Exception("You must specify at least one arg between end_time and duration")

        self._set_start_time(start_time)
        if duration:
            self.duration = duration
            self.end_time = self.start_time + datetime.timedelta(days=duration)
        else:
            self._set_end_time(end_time)
            self.duration = calcDurationInDays(self.end_time, self.start_time)


    def start_time_in_millis(self):
        return calcTimeInMillis(self.start_time)

    def end_time_in_millis(self):
        return calcTimeInMillis(self.end_time)


    ##############################################
    # RELATIONS
    ##############################################
    project = models.ForeignKey('Project')

    # This is the level information. If a task has a parent it is grafted (indentation)
    # into the parent task. Only one task can have parent = null: the root task
    # that is the project task. All other tasks must have a parent.
    parent = models.ForeignKey('self', related_name="grafted_task_set", null=True, blank=True)
    # Calculated @see save. The root task is at level 0 (zero), its children at level 1 (one) and so on.
    # Levels must be consistent with the project structure: you can't have a task of level n+1
    # if you don't have a task of level n above
    level = models.IntegerField()

    # All the tasks that this task must wait for termination before it can start its work.
    # This is not a symmetrical relation
    depends_on = models.ManyToManyField('self', symmetrical=False, through='Dependency')

    # The resources that work on this task
    assigned_to = models.ManyToManyField('Resource', through='Assignment')


    #######################################################################
    # ACTIONS
    #######################################################################

    def addTask(self, name, code, description, row_index, start_time, end_time=None, duration=None, status=None, progress=None, depends_on=None):
        """
        Add a new task
        :argument depends_on can be a task or a list of task that the new task depends on.
        :returns the task created
        """
        task = Task()
        task.name = name
        task.code = code
        task.description = description
        task.row_index = row_index
        task.set_duration(start_time, duration=duration, end_time=end_time)

        if status:
            task.status = status
        if progress:
            task.progress = progress
        if depends_on:
            if isinstance(depends_on, list):
                pass
            elif isinstance(depends_on, Task):
                pass

        # RELATIONS
        task.project = self.project
        task.parent = self

        task.save()

        return task

    def removeTask(self, taskId):
        """
        Delete a grafted task identified by the taskId
        """
        self.grafted_task_set.get(pk=taskId).delete()

    def addDependency(self, taskId, delay=None):
        """
        Add a dependency between the task itself (start_task) and the task identified by taskId (finish_task).
        """
        dep = Dependency()
        dep.start_task = self

        # TODO addDependency Add business rule here
        dep.finish_task = self.project.task_set.get(pk=taskId)

        if delay:
            dep.delay = delay

        dep.save()

    def removeDependency(self, taskId):
        """
        Remove the dependency this task has with the task identified by taskId
        """
        self.dependency_set.filter(finish_task__id=taskId).delete()

    def addAssignment(self, resource, effort=None):
        """
        Add a resource assigned to this task. Optionally can be inserted also the effort already done
        """
        asgn = Assignment()
        asgn.resource = resource
        asgn.task = self

        if effort:
            asgn.effort = effort

        asgn.save()

    def removeAssignment(self, resourceId):
        """
        Remove the resource's assignment from this task
        """
        self.assignment_set.get(resource__id=resourceId).delete()


    def clean(self):

        # validate_row_index
        task = self.project.task_set.filter(row_index=self.row_index)
        if task:
            if task.count() > 1 or task.first().id != self.id:
                raise ValidationError("Task with row index {0} already exist in this project".format(self.row_index))

    def save(self, **kwargs):

        self.level = self.parent.level+1 if self.parent else 0

        super(Task, self).save(**kwargs)


    def __unicode__(self):
        return u"{name} ({code}): progression: {prog}%".format(name=self.name,
                                                              code=self.code,
                                                              prog=self.progress)


class Dependency(models.Model):
    """
    Many to many relationship between tasks. One task can start only when zero or more tasks are finished.
    It is not merely a matter of time, in fact some tasks can start only after other tasks are finished AND after a delay.
    """
    start_task = models.ForeignKey('Task', related_name="dependency_set")
    finish_task = models.ForeignKey('Task', related_name="+")
    delay = models.IntegerField(default=0)

    class Meta:
        # One task can be dependent on another task only once!
        unique_together = ("start_task", "finish_task")
        verbose_name_plural = "Dependencies"


    def __unicode__(self):
        return u"start_task: {}, finish_task: {} with {} delay".format(self.start_task, self.finish_task, self.delay)


class Resource(models.Model):
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u"{name} {surname}".format(name=self.user.first_name, surname=self.user.last_name)


class Assignment(models.Model):
    resource = models.ForeignKey('Resource')
    task = models.ForeignKey('Task')

    # TODO Need to add a role for the assignment. After adding a role change the task's actions
    # A resource can be a project manager on a project and can be a developer on another project?

    effort = models.IntegerField(default=0)  # time in millis


###################################################################
# EVENTS
###################################################################

@receiver(post_save, sender=Project)
def after_save_project(sender, instance, created, **kwargs):
    if (created and instance.id is not None):
        root_task = Task()
        root_task.project = instance
        root_task.name = instance.name
        root_task.code = "{prj_name}_root".format(prj_name=instance.name)
        root_task.row_index = 0
        root_task.parent = None
        root_task.set_duration(instance.start_time, end_time=instance.end_time)
        root_task.save()

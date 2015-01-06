import datetime
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from pip.wheel import root_is_purelib
from gantt.models import Project, Task, Resource, Dependency, Assignment


def initModel():

    u = User.objects.create_user("pippo")
    r = Resource(user=u)
    r.save()

    p = Project()
    p.name = "Gant Testing"
    p.start_time = timezone.now()
    p.end_time = p.start_time + datetime.timedelta(days=60)

    p.save()

    r.work_on.add(p)


def clearModel():

    Project.objects.all().delete()
    Resource.objects.all().delete()



class TaskTestCase(TestCase):

    def setUp(self):
        initModel()
        self.project = Project.objects.all()[0] #Only one project must be in the db for this TestCase
        self.resource = Resource.objects.all()[0]

    def tearDown(self):
        clearModel()

    def _createTasksArgs(self, number=0):
        args = dict()
        args['name']="write init model"+str(number)
        args['code']="inimod"+str(number)
        args['description'] = "descr"+str(number)
        args['row_index']=1+number
        args['start_time']=timezone.now() + datetime.timedelta(days=number)
        args['end_time']=timezone.now() + datetime.timedelta(days=10+number)

        return args


    def test_addTask(self):

        root_task = self.project.root_task
        t= root_task.addTask(**self._createTasksArgs())

        self.assertEqual(t, root_task.grafted_task_set.first())
        self.assertEqual(self.project.task_set.count(), 2)

    def test_removeTask(self):

        root_task = self.project.root_task
        t= root_task.addTask(**self._createTasksArgs())
        root_task.removeTask(t.id)

        try:
            Task.objects.get(id=t.id)
            self.assertTrue(False)
        except Task.DoesNotExist:
            self.assertTrue(True)

        self.assertEqual(self.project.task_set.count(), 1)

    def test_addDependency(self):

        root_task = self.project.root_task
        t1= root_task.addTask(**self._createTasksArgs())

        root_task = self.project.root_task
        t2= root_task.addTask(**self._createTasksArgs(10))

        t2.addDependency(t1.id)

        self.assertEqual(t2.depends_on.count(), 1)
        self.assertEqual(t2.depends_on.first(), t1)

    def test_removeDependency(self):

        root_task = self.project.root_task
        t1= root_task.addTask(**self._createTasksArgs())

        root_task = self.project.root_task
        t2= root_task.addTask(**self._createTasksArgs(10))

        t2.addDependency(t1.id)

        t2.removeDependency(t1.id)

        self.assertEqual(t2.depends_on.count(), 0)
        self.assertEqual(self.project.task_set.get(pk=t1.id),t1)

    def test_addAssignment(self):

        root_task = self.project.root_task
        root_task.addAssignment(self.resource)

        self.assertEqual(root_task.assigned_to.count(), 1)

    def test_removeAssignment(self):

        root_task = self.project.root_task
        root_task.addAssignment(self.resource)

        root_task.removeAssignment(self.resource.id)

        self.assertEqual(root_task.assigned_to.count(), 0)

    def test_delete_project(self):

        root_task = self.project.root_task
        t1= root_task.addTask(**self._createTasksArgs())

        root_task = self.project.root_task
        t2= root_task.addTask(**self._createTasksArgs(10))

        t2.addDependency(t1.id)

        root_task = self.project.root_task
        root_task.addAssignment(self.resource)

        self.project.delete()

        self.assertEqual(Task.objects.count(),0)
        self.assertEqual(Dependency.objects.count(),0)
        self.assertEqual(Assignment.objects.count(),0)

    def test_delete_root_task(self):

        root_task = self.project.root_task
        t1= root_task.addTask(**self._createTasksArgs())

        root_task = self.project.root_task
        t2= root_task.addTask(**self._createTasksArgs(10))

        t2.addDependency(t1.id)

        root_task = self.project.root_task
        root_task.addAssignment(self.resource)

        root_task.delete()

        self.assertEqual(Task.objects.count(),0)
        self.assertEqual(Dependency.objects.count(),0)
        self.assertEqual(Assignment.objects.count(),0)





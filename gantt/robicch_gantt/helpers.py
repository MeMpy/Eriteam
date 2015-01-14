#Before to ask any questions read this:
# http://roberto.open-lab.com/2012/08/24/jquery-gantt-editor/
from gantt.models import Resource, Task


def find_parent(i, t, tasks):
    """
    scan the tasks array from the actual task (i) to the first one (the root task level 0)
    searching for the first task with a level lesser than the actual task's level.
    This task, if exists, is the parent task. If it doesn't exist the actual task is a root task.
    Return the index of the parent task if exists None otherwise
    """

    if t['level']==0:
        #this is the root task, there is no parent
        return None
    # find the parent
    j = i - 1
    while not tasks[j]['level'] < t['level']:
        j = j - 1
    #this is the parent
    return j

def get_task(project, t):
    """
    Get the task from the project's task_Set. Return the task
    Returns None if no task can be found
    """
    if isinstance(t['id'], int):
        try:
            task = project.task_set.get(pk=t['id'])
        except Task.DoesNotExist:
            task=None
    else:
        task=None

    return task

def save_task(project, t, i, tasks):
    """
    Recursive function used to save the tasks array.
    A task can have two states:
    it exists already in the db (id is a int)
    it is new (id is a string starting with tmp)
    if it already exists we simply update each fields.
    if it is new we have to find the parent and and with it we can insert the task.

    The recursion step lies in the fact that the parent can be a new task, for this reason we have to call recursively
    save_task in order to save each parent before adding their children.

    The flag save is used in order to avoid useless saves
    """

    #base step
    if 'saved' in t:
        return project.task_set.get(pk=t['id'])

    j = find_parent(i, t, tasks)

    #recursion step
    if j is not None:
        t_parent = tasks[j]
        if isinstance(t_parent['id'], int):
            task_parent = project.task_set.get(pk=t_parent['id'])
        else:
            #recursion
            task_parent = save_task(project, t_parent, j, tasks)
    else:
        task_parent = None

    #base step
    task= get_task(project,t)
    #the task already exists, we need to update it
    if task:
        #keys: [u'status', u'assigs', u'hasChild', u'code', u'end', u'description', u'level', u'startIsMilestone',
        # u'start', u'depends', u'canWrite', u'duration', u'progress', u'endIsMilestone', u'id', u'name']
        task.status = t['status']
        task.name = t['name']
        task.code = t['code']
        task.set_duration(t['start'], duration=t['duration'])
        task.description = t['description']
        task.progress = t['progress']

        task.row_index = i

        task.parent = task_parent

        task.save()
        t['saved'] = True

    else:
        #keys: [u'status', u'assigs', u'hasChild', u'code', u'end', u'description', u'level', u'startIsMilestone',
        # u'start', u'depends', u'canWrite', u'duration', u'progress', u'endIsMilestone', u'id', u'name']
        task=task_parent.addTask(
                t['name'],
                t['code'],
                t['description'],
                i,
                t['start'],
                t['end'],
                t['duration'],
                t['status'],
                t['progress']
                )
        t['id'] = task.id
        t['saved'] = True

    return task


def save_dependencies(instance, t, tasks):
    """
    For each task we rebuild its dependency parsing the depends field.
    """

    #reset all current dependencis
    task = instance.task_set.get(pk=t['id'])
    task.dependency_set.all().delete()

    if t['depends']:
        #there are some dependencies
        deps = t['depends'].split(',')
        for d in deps:
            if ':' in d:
                dep_id = tasks[int(d[:d.index(':')])]['id']
                dep_delay = int(d[d.index(':')+1:])
                task.addDependency(dep_id,dep_delay)
            else:
                dep_id = tasks[int(d)]['id']
                task.addDependency(dep_id)


def save_assignments(instance, t):
    """
    For each task we rebuild its assignments
    """

    #reset all current assignments
    task = instance.task_set.get(pk=t['id'])
    task.assignment_set.all().delete()

    if t['assigs']:
        for ass in t['assigs']:
            r = Resource.objects.get(pk=ass['resourceId'])
            task.addAssignment(r, ass['effort'])
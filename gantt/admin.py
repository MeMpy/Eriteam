from django.contrib import admin

# Register your models here.
from gantt.models import Project, Resource, Task, Dependency, Assignment


class ProjectAdmin(admin.ModelAdmin):
    exclude = ('duration',)

class TaskAdmin(admin.ModelAdmin):
    exclude = ('duration','level')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Resource)
admin.site.register(Task,TaskAdmin )
admin.site.register(Dependency)
admin.site.register(Assignment)
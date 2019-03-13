from django.contrib import admin
from task_manager.models import Employee, Project, Task


admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Task)
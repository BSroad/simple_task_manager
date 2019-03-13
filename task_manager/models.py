from django.db import models
from django.contrib.auth.models import User
import uuid


class Employee(models.Model):
    user_internal = models.OneToOneField(User, on_delete=models.CASCADE)

#     project = models.ManyToManyField(Project)
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)

    def __str__(self):
        return self.user_internal.username

    def get_id(self):
        return self.id

    def get_name(self):
        self.user_internal.username


class Project(models.Model):
    title = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=200, default='')
    project_uid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    def __str__(self):
        return self.title


class Task(models.Model):
    """Task have 1 assigned person and assigned to the Project"""
    title = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=200, default='')
    due_date = models.DateTimeField(auto_now_add=False)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    assigned_person = models.ForeignKey(Employee,on_delete=models.CASCADE)
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)

    def __str__(self):
        return self.title


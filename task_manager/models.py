from django.db import models
from django.contrib.auth.models import User
import uuid


class EmployeeManager(models.Manager):
    def create_new_user(self, user_internal, is_manager, is_developer):
        new_user = self.create(user_internal=user_internal, is_manager=is_manager,
                               is_developer=is_developer)
        return new_user


class Employee(models.Model):
    user_internal = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    objects = EmployeeManager()

    def __str__(self):
        return self.user_internal.username

    def get_id(self):
        return self.id

    def get_name(self):
        return self.user_internal.username


class ProjectManager(models.Manager):
    def create_new_project(self, title, description):
        new_project = self.create(title=title, description=description)
        return new_project

class Project(models.Model):
    title = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=200, default='')
    project_uid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    objects = ProjectManager()

    def __str__(self):
        return self.title


class Task(models.Model):
    """Task have 1 assigned person and assigned to the Project"""
    title = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=200, default='')
    due_date = models.DateTimeField(auto_now_add=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_person = models.ForeignKey(Employee,on_delete=models.CASCADE)
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)

    def __str__(self):
        return self.title


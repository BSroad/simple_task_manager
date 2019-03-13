from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

#     project = models.ManyToManyField(Project)
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

# class Manager(Person):
#     class Meta:
#         permissions = (
#             ("can_create", "Can create"),
#             ("can_read", "Can read"),
#             ("can_update", "Can update"),
#             ("can_delete", "Can delete"))


class Project(models.Model):
    title = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title


class Task(models.Model):
    """Task have 1 assigned person and assigned to the Project"""
    title = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=200, default='')
    due_date = models.DateTimeField(auto_now_add=False)
    project = models.ManyToManyField(Project)
    assigned_person = models.OneToOneField(Employee, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title


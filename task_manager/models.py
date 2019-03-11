from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_person = models.ForeignKey(Person, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import json

from . import models


def index(request):
    """Home page for app task_manager"""
    return render(request, 'task_manager/index.html')


def logout_view(request):
    """Finish session of app"""
    logout(request)
    return HttpResponseRedirect(reverse('task_manager:index'))


def register(request):
    """Register new user"""
    if request.method != 'POST':
        # Display blank registration form
        form = UserCreationForm()
    else:
        # Processing of fulfilled form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Login and redirection on homepage
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'],)
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('task_manager:index'))
    context = {'form': form}
    return render(request, 'task_manager/register.html', context)


def employee_position_check(user):
    try:
        employee = models.Employee.objects.get(user=user)
        if employee.is_manager:
            return True
        else:
            return False
    except:
        return render(request, 'task_manager/index.html')

#
@login_required
# @user_passes_test(employee_position_check, redirect_field_name='REDIRECT_FIELD_NAME')  # Set redirect_field_name=REDIRECT_FIELD_NAME

def task_view(request):
    try:
        employee = models.Employee.objects.get(user=request.user)
        tasks = models.Task.objects.filter(assigned_person=employee)
        length_dict = [len(entry) for entry in tasks.values()]
        dict = [entry for entry in tasks.values()]
        developers = models.Employee.objects.filter(is_developer=True)
        projects = models.Project.objects.all()
        all_tasks = models.Task.objects.all()

        if employee_position_check(request.user) == False:
            if len(length_dict) > 0:

                return render(request, 'task_manager/developer_task_view.html',
                      {'tasks': dict})
            else:
                return render(request, 'task_manager/empty_task_view.html',)
        elif employee_position_check(request.user) == True:
            return render(request, 'task_manager/manager_task_view.html',
                      {'tasks': dict,'developers':developers,
                       'projects': projects, 'all_tasks': all_tasks})
        else:
            return render(request, 'task_manager/index.html')
    except:
        return render(request, 'task_manager/index.html')

#######################################################################
from django.http import JsonResponse


def tasks_for_user(request):
    if request.method == "GET":
        received_json_data = json.loads(request.body)
        # {'user_id': '123243-2535235-235235-23523'}
        requested_Employee = models.Employee.objects.filter(
            user_id=received_json_data['user_id'])
        tasks_list = models.Task.objects.filter(
            assigned_person=requested_Employee)
        response_json = {'task_list':[]}
        for task in tasks_list:
            response_json['task_list'] = \
                response_json['task_list'].append(
                    {"title": task.title, "ID": task.task_id})
        return JsonResponse(response_json)


# Return response about all developers in DB
def developers_list(request):
    if request.method == "GET":
        developers_list = models.Employee.objects.filter(is_developer=True)
        response_developers = []
        for developer in developers_list:
            response_developers.append({"user_name": str(developer),"ID": developer.id})
        return JsonResponse({"developers": response_developers})


# Return response about all projects in DB
def all_projects(request):
    if request.method == "GET":
        projects = models.Project.objects.all()
        response_projects = []
        for project in projects:
            response_projects.append({"project name": str(project),
                                      "ID": project.project_uid})
        return JsonResponse({"projects": response_projects})


# Return response about all tasks in DB
def all_tasks(request):
    if request.method == "GET":
        all_tasks = models.Task.objects.all()
        response_tasks = []
        for task in all_tasks:
             response_tasks.append({"task title": str(task),
                                   "task id": task.task_id,
                                   "related project": task.project.title,
                                   "assigned person": task.assigned_person.get_id(),
                                   "task description": task.description,
                                   "due date": task.due_date,
                                   })
        return JsonResponse({"tasks": response_tasks})


# функция, которая создаст нового usera --> employee
#
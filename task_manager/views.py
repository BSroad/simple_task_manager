from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
import json

from . import models


def index(request):
    """Home page for app task_manager"""
    return render(request, 'task_manager/index.html')


def api_login(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        username = received_json_data["username"]
        password = received_json_data["password"]
        authenticated_user = authenticate(username=username,
                                          password=password, )
        if authenticated_user is not None:
            if authenticated_user.is_active:
                request.session.set_expiry(
                    86400)  # sets the exp. value of the session
                login(request, authenticated_user)  # the user is now logged in
                return JsonResponse({"error": "success"})
            else:
                return JsonResponse({"error": "user is not active"})
        else:
            return JsonResponse({"error": "wrong credentials"})
    else:
        return JsonResponse({"error": "Wrong request type, try POST"})


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


def create_new_employee(request):
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        user_internal = received_json_data["user_internal"]
        if user_internal is not None:
            user_internal_object = models.User.objects.get(username = received_json_data["user_internal"])
            try:
                new_user = models.Employee.objects.create_new_user(user_internal_object,
                                                                   received_json_data["is_manager"],
                                                                   received_json_data["is_developer"])
                new_user.save()
            except IntegrityError as e:
                return JsonResponse({"error" : "Employee with this user already exists"})
            return JsonResponse({"new user id ": str(new_user.get_id())})
        else:
            return JsonResponse({"error" : "User doesn't exist"})
    return JsonResponse({"error" : "Try POST request"})


def create_new_user(request):
    received_json_data = json.loads(request.body)
    if not all(keys in received_json_data for keys in ("username", "email", "password")):
        return JsonResponse({"error" : "request doesn't contain username, email, or password"})
    try:
        user = User.objects.create_user(username=received_json_data["username"],
                                        email=received_json_data["email"],
                                        password=received_json_data["password"])
        user.save()
        return JsonResponse({"username": user.username })
    except IntegrityError as e:
        return JsonResponse(
            {"error": "User with this username already exists"})


def update_user(request):
    received_json_data = json.loads(request.body)
    username = received_json_data["username"]
    user = User.objects.get(username=username)
    if user is None:
        return JsonResponse({"error" : "User with this name does not exist"})
    if "email" in received_json_data:
        email = received_json_data["email"]
        user.email = email
    if "password" in received_json_data:
        password = received_json_data["password"]
        user.password = password
    user.save()
    return JsonResponse({"username": user.username, "email":user.email})


def delete_user(request):
    received_json_data = json.loads(request.body)
    username = received_json_data["username"]
    user = User.objects.get(username=username)
    if user is None:
        return JsonResponse({"error": "User with this name does not exist"})
    user.delete()
    return JsonResponse({"success" : True})


def get_user(request):
    received_json_data = json.loads(request.body)
    username = received_json_data["username"]
    user = User.objects.get(username=username)
    if user is None:
        return JsonResponse({"error": "User with this name does not exist"})
    return JsonResponse({"username": user.username, "email": user.email})


def CRUD_user(request):
    if request.method == "POST":
        return create_new_user(request)

    if request.method == "PUT":
        return update_user(request)

    if request.method == "DELETE":
        return delete_user(request)

    if request.method == "GET":
        return get_user(request)
    return JsonResponse({"error" : "wrong HTTP request type"})
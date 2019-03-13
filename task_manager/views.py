from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

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
        return None

#
@login_required
# @user_passes_test(employee_position_check, redirect_field_name='REDIRECT_FIELD_NAME')  # Set redirect_field_name=REDIRECT_FIELD_NAME

def task_view(request):
    employee = models.Employee.objects.get(user=request.user)
    tasks = models.Task.objects.filter(assigned_person=employee)
    if employee_position_check(request.user) == False:
        return render(request, 'task_manager/developer_task_view.html',
                  {'tasks': [entry for entry in tasks.values()]}) # Узнать длинну, поустой или нет
    elif employee_position_check(request.user) == True:
        return render(request, 'task_manager/manager_task_view.html',
                  {'tasks': [entry for entry in tasks.values()]})
    else:
        return render(request, 'task_manager/index.html')



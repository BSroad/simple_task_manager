from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
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
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('task_manager:index'))
    context = {'form': form}
    return render(request, 'task_manager/register.html', context)
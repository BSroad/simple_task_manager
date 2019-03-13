"""Define URL for task_manager app"""
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from . import forms


app_name = 'task_manager'

urlpatterns = [
    # url for home page
    path('', views.index, name='index'),

    # urls for login, logout and register pages

    path('login/', LoginView.as_view(
        template_name='task_manager/login.html',
        authentication_form=forms.CustomAuthenticationForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('task_view/', views.task_view, name='task_view'),
    # path('task_view/', views.task_view, name='task_view'),


]

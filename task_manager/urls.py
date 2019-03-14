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
    path('api_login/', views.api_login,  name='api_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # url for users to preview their profile (assigned tasks and projects)
    path('task_view/', views.task_view, name='task_view'),
    # path('tasks_for_user/', views.tasks_for_user, name= 'tasks_for_user'),

    # REST-ish style request urls
    path('developers_list/', views.developers_list, name='developers_list'),
    path('all_projects/', views.all_projects, name='all_projects'),
    path('all_tasks/', views.all_tasks, name='all_tasks'),
    path('crud_user/', views.CRUD_user, name='crud_user'),
    path('create_new_employee/', views.create_new_employee, name='create_new_user'),
]

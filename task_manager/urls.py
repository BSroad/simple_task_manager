"""Define URL for task_manager app"""
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'task_manager'

urlpatterns = [
    # url for home page
    path('', views.index, name='index'),

    # urls for login and register pages

    path('login/', LoginView.as_view(
        template_name='task_manager/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

]

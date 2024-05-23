"""
URL configuration for todoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testApp import admin_users, auth, home, user_category

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', auth.login),
    path('logout', auth.logout),
    path('register', auth.register),
    path('tasks', home.index, name="home"),
    path('tasks/<int:task_id>/', home.get_task, name='get_task'),
    path('categories', user_category.index ),
    path('categories/<int:category_id>/', user_category.get_category),
    path('administrator/users', admin_users.index),
    path('administrator/users/<int:user_id>/', admin_users.get_user),
]

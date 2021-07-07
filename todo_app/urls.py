"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home ,name='home'),

    #AUTH
    path('signup/',views.signupuser ,name='signupuser'),
    path('login/',views.loginuser ,name='loginuser'),
    path('logout/',views.logoutuser ,name='logoutuser'),

    #TODOS
    path('create/',views.create_todos ,name='create_todos'),
    path('current/',views.current_todos ,name='current_todos'),
    path('completed/',views.completed_todos ,name='completed_todos'),
    path('todo/<int:todo_pk>',views.view_todos ,name='view_todos'),
    path('todo/<int:todo_pk>/complete',views.complete_todos ,name='complete_todos'),
    path('todo/<int:todo_pk>/delete',views.delete_todos ,name='delete_todos'),
]

"""job_portal_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from job_portal_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index_fun),
    path('user_register',views.user_register_fun),
    path('save_job',views.save_job,name="save_job"),
    path('delete_saved_job',views.delete_saved_job,name="delete_saved_job"),
    path('view_saved_jobs',views.view_saved_jobs_fun,name="view_saved_jobs"),
    path('user_login',views.user_login_fun,name="user_login"),
    path('user_logout',views.user_logout_fun),
    path('index',views.index_fun,name="index"),
    path('about',views.about_fun),
    path('contact',views.contact_fun),
    path('find_job_list',views.find_job_list_fun,name='find_job_list'),
    path('filter_job_list',views.filter_job_list_fun,name='filter_job_list')
]

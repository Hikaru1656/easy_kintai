"""easy_kintai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from . import views


urlpatterns = [
    path('owner/attends/', views.attends, name='attends'),
    path('user/check/', views.check, name='check'),
    path('owner/payments/', views.payments, name='payments'),
    path('owner/schedule/', views.schedule, name='schedule'),
    path("owner/schedule/add/", views.add_event, name="add_event"),
    path("owner/schedule/list/", views.get_event, name="get_event"),
    path("owner/employees", views.employees, name="employees"),

]

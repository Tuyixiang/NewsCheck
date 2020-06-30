"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.http import JsonResponse
from . import database
from threading import Thread
from time import sleep


def schedule():
    while True:
        sleep(86400)
        database.update()


Thread(target=schedule).start()


def home(request):
    return JsonResponse(database.fetch())


def access(request):
    database.mark_read(request.GET['key'], request.GET['url'])
    return JsonResponse({})


def remove(request):
    database.remove(request.GET['key'])
    return JsonResponse({})


def add(request):
    database.add(request.GET['key'], request.GET['strict'])
    return JsonResponse({})


def ls(request):
    return JsonResponse({'data': database.ls()})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('access', access),
    path('remove', remove),
    path('add', add),
    path('ls', ls),
]

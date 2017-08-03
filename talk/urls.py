"""StudentManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from talk import views


urlpatterns = [
    url(r'^$', views.user_list, name='user_list'),
    url(r'^log_in/', views.log_in, name='log_in'),
    url(r'^log_out/', views.log_out, name='log_out'),
    url(r'^sign_up/', views.sign_up, name='sign_up'),
]

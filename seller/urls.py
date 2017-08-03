from django.conf.urls import url, include
from django.contrib import admin
from seller import views

urlpatterns = [
    url(r'^', views.index, name='seller'),
]

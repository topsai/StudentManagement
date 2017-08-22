from django.conf.urls import url, include
from django.contrib import admin
from myadmin import views

urlpatterns = [
    url(r'^$', views.index, name='manage'),
    url(r'^(\w+)/(\w+)/$', views.table_obj_list, name='table_obj'),
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name='table_obj_add'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name='table_obj_change'),
    url(r'^(\w+)/(\w+)/(\d+)/change/delete/$', views.table_obj_change_delte, name='table_obj_change_delete'),
    url(r'^test/$', views.test, name='test111'),
    url(r'^(\w+)/$', views.app_obj, name='app_obj'),

]

from django.conf.urls import url, include
from django.contrib import admin
from manage import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^students/', views.students),
    url(r'^logout/', views.logout),
    url(r'^regist/', views.regist),
    url(r'^$', views.manage),
]

from django.conf.urls import url, include
from django.contrib import admin
from manage import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.manage, name='user_list'),
]

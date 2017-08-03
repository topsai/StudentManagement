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

from manage import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^manage/', include('myadmin.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^seller/', include('seller.urls')),
    # url(r'^student/$', include('student.urls'), ),
    # url(r'^$', views.index),
    # url(r'^login/', views.login, name='log_in'),
    # url(r'^regist/', views.regist, name='sign_up'),
    # url(r'^talk/', views.talk, name='talksb'),
    # url(r'^$', include('talk.urls')),
    url(r'^my/', include('myadmin.urls')),
    # url(r'^', include('myadmin.urls')),
    # url(r'blog/$', livelog, name='livelog'),
    # url(r'blog/websocket/$', ws),
    # url('^', include('django.contrib.auth.urls'))
    # url(r'^accounts/login/$', auth_views.login, {'template_name': 'myapp/login.html'}),
]

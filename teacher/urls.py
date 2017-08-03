from django.conf.urls import url, include
from django.contrib import admin
from teacher import views
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^manage/', include('backend.urls')),
    url(r'^$', views.index, name='teacher'),
]

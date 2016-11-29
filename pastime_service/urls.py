import django.contrib.auth.views

from django.conf.urls import url, include
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.logUserIn, name='logUserIn'),
    url(r'^logout/$', views.logUserOut, name='logUserOut'),
    # url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^$', views.index, name='index'),
]

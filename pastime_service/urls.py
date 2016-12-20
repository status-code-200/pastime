from django.conf.urls import url, include
import django.contrib.auth.views
from django.contrib import admin

from . import views
from .forms import EventFormTemplate, RegistrationFormTemplate


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/$',django.contrib.auth.views.login, {'template_name': 'pastime_service/login.html'}, name = 'login'),
    url(r'^login/$', views.log_user_in, name='logUserIn'),
    url(r'^logout/$', views.log_user_out, name='logUserOut'),
    url(r'^create_event/$', EventFormTemplate.as_view(), name='create_event'),
    url(r'^registration/$', RegistrationFormTemplate.as_view(), name='registration'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^join_event/$', views.join_event, name='join_event'),

    url(r'^$', views.index, name='index'),
]

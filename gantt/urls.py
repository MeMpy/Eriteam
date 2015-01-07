from django.conf.urls import patterns, url, include
from gantt import views

urlpatterns = patterns('',


    url(r'robicch/', include('gantt.robicch_gantt.urls', namespace='robicch')),
    url(r'api/project/(?P<project_id>\d+)/$', views.TaskList.as_view(), name='api_get' ),




)

from django.conf.urls import patterns, url
from gantt.robicch_gantt import views

urlpatterns = patterns('',


    url(r'api/project/(?P<project_id>\d+)/$', views.TaskListRob.as_view(), name='api_get' ),
    url(r'api/project/(?P<project_id>\d+)/task$', views.TaskDetailRob.as_view(), name='api_post' ),
    url(r'chart/(?P<project_id>\d+)/$', views.robicch_gantt, name='chart'),


)
from django.conf.urls import patterns, url
from gantt.robicch_gantt import views

urlpatterns = patterns('',


    url(r'api/project/(?P<project_id>\d+)/$', views.TaskListRob.as_view() ),
    url(r'api/project/(?P<project_id>\d+)/task$', views.TaskDetailRob.as_view() ),
    url(r'chart/$', views.robicch_gantt),


)
from django.contrib import admin
from django.urls import path,re_path
from  . import views


urlpatterns = [

    path('', views.index,name='index'),
    re_path(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    re_path(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    re_path(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),


]

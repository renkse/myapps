__author__ = 'renkse'
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
)
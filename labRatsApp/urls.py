from django.conf.urls import patterns, url
from labRatsApp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
	url(r'^register/$', views.signUp, name = 'signUp')
)

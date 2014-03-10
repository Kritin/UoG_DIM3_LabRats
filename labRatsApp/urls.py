from django.conf.urls import patterns, url
from labRatsApp import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.signUp, name = 'signUp'),
	url(r'^login/$', views.user_login, name = 'login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^restricted/$', views.restricted, name='restricted'),
	url(r'^about/$', views.about, name='about'),
	url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
	url(r'^createExperiment/(?P<username>\w+)/$', views.createExperiment, name='createExperiment'),
	url(r'^experiment/(?P<expId>\w+)/$', views.experimentPage, name='experimentPage'),
	url(r'^experiment/(?P<eID>\w+)/(?P<status>\w+)/(?P<username>\w+)/$', views.modifyParticipantStatus, name='modifyParticipantStatus'),
	url(r'^editProfile/$', views.editUserDetail, name='editUserDetail'),
	url(r'^searchExperiment/$', views.searchExperiment, name='searchExperiment')    
)

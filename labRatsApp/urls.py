from django.conf.urls import patterns, url
from labRatsApp import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.signUp, name = 'signUp'),
	url(r'^login/$', views.user_login, name = 'login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^about/$', views.about, name='about'),
	url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
	url(r'^experiment/create/$', views.createExperiment, name='createExperiment'),
	url(r'^experiment/modify/(?P<expId>\w+)/$', views.modifyExperiment, name='modifyExperiment'),
	url(r'^experiment/(?P<expId>\w+)/$', views.experimentPage, name='experimentPage'),
	url(r'^experiment/(?P<eID>\w+)/enrolto/(?P<tID>\w+)/$', views.enrol, name='enrol'),
	url(r'^experiment/(?P<eID>\w+)/setstatus/(?P<status>\w+)/user/(?P<username>\w+)/$', views.modifyParticipantStatus, name='modifyParticipantStatus'),
	url(r'^editProfile/$', views.editUserDetail, name='editUserDetail'),
	url(r'^search/$', views.search, name='search'),
	url(r'^tag/(?P<tag>\w+)/$', views.tag, name='tag'),
	url(r'^bid/(?P<expId>\w+)/$', views.bid, name='bid')  
)

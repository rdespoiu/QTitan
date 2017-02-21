# Django Imports
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

# View definitions
from . import views


# URL Configuration
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register/', views.register, name = 'register'),
    url(r'^login/', auth_views.login, {'template_name': 'QTSurvey/login.html'}, name = 'login'),
    url(r'^logout/$', auth_views.logout, { 'next_page': views.index }, name = 'logout'),
    url(r'^surveys/', views.surveys, name = 'surveys'),
    url(r'^analytics/', views.researcher_analytics, name = 'analytics'),
    url(r'^subjects/', views.researcher_subjects, name = 'subjects'),
    url(r'^completed/', views.subject_completed_surveys, name = 'completed'),
    url(r'^create/', views.create_survey, name = 'create'),
    url(r'^takesurvey/(?P<survey_id>\w{0,50})/$', views.take_survey, name='takesurvey'),
<<<<<<< HEAD
    url(r'^delete/(?P<pk>\d+)/$', views.SurveyDelete.as_view(), name='delete_survey'),
=======
    url(r'^viewresponse/(?P<survey_id>\w{0,50})/$', views.view_survey_self_response, name='viewresponse'),
    url(r'^viewresults/(?P<survey_id>\w{0,50})/$', views.researcher_view_results, name='viewresults'),
>>>>>>> origin/master
]

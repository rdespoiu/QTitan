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
    url(r'^logout/$', auth_views.logout, name = 'logout'),
    url(r'^surveys/', views.surveys, name = 'surveys'),
    url(r'^analytics/', views.researcher_analytics, name = 'analytics'),
    url(r'^subjects/', views.researcher_subjects, name = 'subjects'),
    url(r'^completed/', views.subject_completed_surveys, name = 'completed'),
    url(r'^create/', views.create_survey, name = 'create'),
]

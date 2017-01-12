# Django Imports
from django.conf.urls import url

# View definitions
from . import views


# URL Configuration
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
]

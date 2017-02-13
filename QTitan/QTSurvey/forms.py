from django import forms
from datetime import datetime
from QTitan.settings import *
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.conf import settings
from .models import BaseDemographic, Survey, SurveyField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name']

class BaseDemo(forms.ModelForm):
    class Meta:
        model = BaseDemographic
        fields =  ['first_name','last_name','phone','dob']

class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['distribution-flag','survey title','survey description']

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
        fields = ['title', 'description', 'distribution']

class CreateSurveyFieldForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateSurveyFieldForm, self).__init__(*args, **kwargs)
        maxFields = 15
        for i in range(1, maxFields + 1):
            self.fields['field{}'.format(i)] = forms.CharField(
                                                max_length = 256,
                                                label = '',
                                                help_text = '',
                                                required = True if i <= 5 else False,
                                                widget = forms.TextInput(
                                                            attrs = {'type': 'text',
                                                                     'class': 'form-control create-survey-form',
                                                                     'placeholder': 'survey option',
                                                                     'id': 'field{}'.format(i),
                                                                     'name': 'field{}'.format(i),
                                                                     'autocomplete': 'off'}))

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
from .models import BaseDemographic
from .models import Survey, SurveyField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name']
        
class BaseDemo(forms.ModelForm):
    #userID = models.many_to_many(User)
    #user_id = int(request.POST['id'])
    #userID = User.objects.get(id = user_id)
    #userID = request.get_user_id()
    demoId = 1
    #userID = 1
    class Meta:
        model = BaseDemographic
        #userID = forms.ModelChoiceField(queryset= BaseDemographic.objects.all())
        fields =  ['first_name','last_name','phone','dob']
        
class CreateSurveyForm(forms.ModelForm):
    
    
    class Meta:
        model = Survey
        fields = ['distribution-flag','survey title','survey description']


'''
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if username and password:
            user = authenticate(username= username, password= password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(UserLoginForm,self).clean(*args, **kwargs) 
'''

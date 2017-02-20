from django import forms
from ..models import BaseDemographic

class BaseDemographicForm(forms.ModelForm):
    class Meta:
        model = BaseDemographic
        fields =  ['first_name','last_name','phone','dob']

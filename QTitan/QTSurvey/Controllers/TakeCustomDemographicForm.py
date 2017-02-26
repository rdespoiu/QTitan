from django import forms
from ..models import CustomDemographic

class TakeCustomDemographicForm(forms.Form):
    def __init__(self, demographicFields, *args, **kwargs):
        super(TakeCustomDemographicForm, self).__init__(*args, **kwargs)

        for i in range(len(demographicFields)):
            self.fields['demographicfield{}'.format(demographicFields[i].id)] = forms.CharField(
                                                label = '',
                                                help_text = '',
                                                required = True,
                                                widget = forms.TextInput(
                                                            attrs = {'type': 'text',
                                                                     'class': 'form-control create-survey-form',
                                                                     'placeholder': demographicFields[i].value,
                                                                     'id': 'demographicfield{}'.format(i),
                                                                     'name': 'demographicfield{}'.format(i),
                                                                     'autocomplete': 'off'}))

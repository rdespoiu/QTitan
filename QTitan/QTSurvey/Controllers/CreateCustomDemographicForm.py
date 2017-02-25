from django import forms
from ..models import CustomDemographicField

class CreateCustomDemographicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateCustomDemographicForm, self).__init__(*args, **kwargs)
        maxFields = 15
        for i in range(1, maxFields + 1):
            self.fields['demographicfield{}'.format(i)] = forms.CharField(
                                                max_length = 256,
                                                label = '',
                                                help_text = '',
                                                required = False,
                                                widget = forms.TextInput(
                                                            attrs = {'type': 'text',
                                                                     'class': 'form-control create-survey-form',
                                                                     'placeholder': 'demographic question',
                                                                     'id': 'demographicfield{}'.format(i),
                                                                     'name': 'demographicfield{}'.format(i),
                                                                     'autocomplete': 'off'}))

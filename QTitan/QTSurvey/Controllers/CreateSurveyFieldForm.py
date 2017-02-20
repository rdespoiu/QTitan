from django import forms
from ..models import SurveyField

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

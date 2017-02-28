from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from ..models import Survey

class SurveyDelete(DeleteView):
    model = Survey
    success_url = reverse_lazy('index')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

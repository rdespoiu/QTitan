from ..models import *
from django.conrib import messages
from django.shortcuts import render

def createSurveys(request):
    if request.method == 'POST':
        form = CreateSurveyForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Error")
        return redirect('QTSurvey/create-survey.html')
    
    context = {'request': request, 'form': form}
    return HttpResponse(template.render(context,request))

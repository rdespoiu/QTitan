# Django Imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from django.shortcuts import redirect

# Models
from .models import *

# Controllers
from .Controllers import *

# Forms
from .forms import *

# Utility
import datetime
from _datetime import datetime


# Views

# Index only redirects. If there is no user session, redirect to login page.
# If there IS a session, redirect to 'surveys'
def index(request):
    if request.user.is_authenticated():
        if not request.session.get('researcher'):
            request.session['researcher'] = True if len(request.user.groups.filter(name='researcher')) == 1 \
                                                 else False
        return redirect('surveys')
    else:
        return redirect('login')

# Registration
def register(request):
    if request.user.is_authenticated():
        return redirect('index')

    template = loader.get_template('QTSurvey/register.html')

    form = UserForm(request.POST)
    demo_obj = BaseDemo(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            userID = User.objects.get(username=username).pk

            if demo_obj.is_valid():
                demo_obj.save()
                BaseDemographic.objects.update(userID = userID)
                return redirect('login')

            return redirect('QTSurvey/register.html')
        return redirect('QTSurvey/register.html')
    context = {'request': request, 'form': form}
    return HttpResponse(template.render(context,request))

# Surveys (Researcher/Subject)
def surveys(request):
    if not request.user.is_authenticated():
        return redirect('index')

    context = {'request': request}

    if request.session.get('researcher'):
        template = loader.get_template('QTSurvey/researcher-surveys.html')
        context['researcherSurveys'] = getResearcherSurveys(request)
    else:
        template = loader.get_template('QTSurvey/subject-available-surveys.html')
        context['subjectAvailableSurveys'] = getSubjectAvailableSurveys(request)

    return HttpResponse(template.render(context, request))

# Analytics (Researcher)
def researcher_analytics(request):
    if not (request.user.is_authenticated() and request.session.get('researcher')):
        return redirect('index')

    template = loader.get_template('QTSurvey/researcher-analytics.html')

    context = {'request': request, 'researcherSurveys': getResearcherSurveys(request)}

    return HttpResponse(template.render(context, request))

# Subject View (Researcher)
def researcher_subjects(request):
    if not (request.user.is_authenticated() and request.session.get('researcher')):
        return redirect('index')

    template = loader.get_template('QTSurvey/researcher-subjects.html')

    context = {'request': request}

    return HttpResponse(template.render(context, request))

# Completed Surveys (Subject)
def subject_completed_surveys(request):
    if not (request.user.is_authenticated() and not request.session.get('researcher')):
        return redirect('index')

    template = loader.get_template('QTSurvey/subject-completed-surveys.html')

    context = {'request': request, 'subjectCompletedSurveys': getSubjectCompletedSurveys(request)}

    return HttpResponse(template.render(context, request))

# Create Survey (Researcher)
def create_survey(request):
    if not (request.user.is_authenticated() and request.session.get('researcher')):
        return redirect('index')

    template = loader.get_template('QTSurvey/create-survey.html')

    surveyForm = CreateSurveyForm(request.POST)
    surveyFieldsForm = CreateSurveyFieldForm(request.POST)

    if request.method == 'POST':
        if surveyForm.is_valid() and surveyFieldsForm.is_valid():
            # Create Survey
            survey = Survey(ownerID = request.user,
                            title = surveyForm.cleaned_data['title'],
                            description = surveyForm.cleaned_data['description'],
                            distribution = surveyForm.cleaned_data['distribution'])
            survey.save()

            # Create Survey Fields
            data = surveyFieldsForm.cleaned_data

            for i in range(1, 31):
                if data.get('field{}'.format(i)):
                    surveyField = SurveyField(surveyID = survey,
                                              value = data.get('field{}'.format(i)))
                    surveyField.save()

            return redirect('index')

    context = {'request': request, 'surveyForm': surveyForm, 'surveyFieldsForm': surveyFieldsForm}
    return HttpResponse(template.render(context, request))

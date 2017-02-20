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

    userForm = UserForm(request.POST or None)
    demographicsForm = BaseDemographicForm(request.POST or None)

    if request.method == 'POST':
        if userForm.is_valid() and demographicsForm.is_valid():
            userData = userForm.cleaned_data
            demographicsData = demographicsForm.cleaned_data

            # Create User object
            newUser = User(username = userData['username'],
                           first_name = userData['first_name'],
                           last_name = userData['last_name'],
                           email = userData['email'])

            newUser.set_password(userData['password'])

            newUser.save()

            # Create BaseDemographic object
            newUserDemographics = BaseDemographic(userID = newUser,
                                                  first_name = demographicsData['first_name'],
                                                  last_name = demographicsData['last_name'],
                                                  phone = demographicsData['phone'],
                                                  dob = demographicsData['dob'])

            newUserDemographics.save()

            login(request, newUser)
            return redirect('index')

    context = {'request': request, 'userForm': userForm, 'demographicsForm': demographicsForm}
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

    context = {'request': request, 'researcherSubjects': getResearcherSubjects(request)}

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

def take_survey(request, survey_id):
    if not (request.user.is_authenticated() and not request.session.get('researcher')):
        return redirect('index')

    template = loader.get_template('QTSurvey/take-survey.html')
    survey = Survey.objects.get(id = survey_id)
    surveyFields = SurveyField.objects.filter(surveyID = survey)

    takeSurveyForm = TakeSurveyForm(surveyFields, request.POST)

    if request.method == 'POST':
        if takeSurveyForm.is_valid():
            data = takeSurveyForm.cleaned_data
            surveyFieldMap = {}

            for field in takeSurveyForm.hidden_fields():
                # Hacky splicing to get orderPosition
                surveyFieldMap[field.value()] = int(str(field).split('orderPosition="', 1)[1].split('"', 1)[0])


            for field in surveyFieldMap:
                completedSurveyField = CompletedSurvey(surveyID = survey,
                                                       surveyFieldID = SurveyField.objects.get(value = field, surveyID = survey),
                                                       userID = request.user,
                                                       orderPosition = surveyFieldMap[field])

                completedSurveyField.save()

            return redirect('index')

        else:
            raise RuntimeError('Invalid form, please try again')


    context = {'request': request, 'takeSurveyForm': takeSurveyForm, 'survey': survey, 'surveyFields': surveyFields}

    return HttpResponse(template.render(context, request))

def view_survey_self_response(request, survey_id):
    if not (request.user.is_authenticated() and not request.session.get('researcher')):
        return redirect('index')

    template = loader.get_template('QTSurvey/subject-view-survey-response.html')

    survey = Survey.objects.get(id = survey_id)
    completedSurvey = sorted(list(CompletedSurvey.objects.filter(surveyID = survey,
                                                                 userID = request.user)),
                             key = lambda x: x.orderPosition)

    context = {'request': request, 'survey': survey, 'completedSurvey': completedSurvey}

    return HttpResponse(template.render(context, request))

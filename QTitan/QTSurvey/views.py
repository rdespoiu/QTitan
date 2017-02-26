# Django Imports
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
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
    if isAuthenticated(request.user):
        if not isResearcher(request.session):
            setResearcher(request)
        return redirect('surveys')

    return redirect('login')

# Registration
def register(request):
    if isAuthenticated(request.user):
        return redirect('index')

    template = setTemplate('QTSurvey/register.html')

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

    return renderPage(template, context, request)

# Surveys (Researcher/Subject)
def surveys(request):
    if not isAuthenticated(request.user):
        return redirect('index')

    context = {'request': request}

    if isResearcher(request.session):
        template = setTemplate('QTSurvey/researcher-surveys.html')
        context['researcherSurveys'] = getResearcherSurveys(request)
    else:
        template = setTemplate('QTSurvey/subject-available-surveys.html')
        context['subjectAvailableSurveys'] = getSubjectAvailableSurveys(request)

    return renderPage(template, context, request)

# Analytics (Researcher)
def researcher_analytics(request):
    if not (isAuthenticated(request.user) and isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/researcher-analytics.html')

    context = {'request': request, 'researcherSurveys': getResearcherSurveys(request)}

    return renderPage(template, context, request)

# Subject View (Researcher)
def researcher_subjects(request):
    if not (isAuthenticated(request.user) and isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/researcher-subjects.html')

    context = {'request': request, 'researcherSubjects': getResearcherSubjects(request)}

    return renderPage(template, context, request)

# Completed Surveys (Subject)
def subject_completed_surveys(request):
    if not (isAuthenticated(request.user) and not isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/subject-completed-surveys.html')

    context = {'request': request, 'subjectCompletedSurveys': getSubjectCompletedSurveys(request)}

    return renderPage(template, context, request)

# Create Survey (Researcher)
def create_survey(request):
    if not (isAuthenticated(request.user) and isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/create-survey.html')

    surveyForm = CreateSurveyForm(request.POST)
    surveyFieldsForm = CreateSurveyFieldForm(request.POST)
    customDemographicsForm = CreateCustomDemographicForm(request.POST)

    if request.method == 'POST':
        if surveyForm.is_valid() and surveyFieldsForm.is_valid() and customDemographicsForm.is_valid():
            # Create Survey
            survey = Survey(ownerID = request.user,
                            title = surveyForm.cleaned_data['title'],
                            description = surveyForm.cleaned_data['description'],
                            distribution = surveyForm.cleaned_data['distribution'],
                            consentneeded = surveyForm.cleaned_data['consentneeded'])
            survey.save()

            # Create Survey Fields
            data = surveyFieldsForm.cleaned_data

            # Create CustomDemographic Fields
            demographicData = customDemographicsForm.cleaned_data

            for i in range(1, 16):
                if data.get('field{}'.format(i)):
                    surveyField = SurveyField(surveyID = survey,
                                              value = data.get('field{}'.format(i)))
                    surveyField.save()

                if demographicData.get('demographicfield{}'.format(i)):
                    demographicField = CustomDemographicField(surveyID = survey,
                                                              value = demographicData.get('demographicfield{}'.format(i)))
                    demographicField.save()

            return redirect('index')

    context = {'request': request, 'surveyForm': surveyForm, 'surveyFieldsForm': surveyFieldsForm, 'customDemographicsForm': customDemographicsForm}

    return renderPage(template, context, request)

def take_survey(request, survey_id):
    if not (isAuthenticated(request.user) and not isResearcher(request.session)):
        return redirect('index')


    template = setTemplate('QTSurvey/take-survey.html')

    survey = Survey.objects.get(id = survey_id)

    if survey.distribution and not hasAccess(request.user, survey):
        return redirect('index')

    if survey.consentneeded and not hasGivenIRBConsent(request.user, survey):
        return redirect('/irbconsent/{}'.format(survey_id))

    surveyFields = getSurveyFields(survey)

    takeSurveyForm = TakeSurveyForm(surveyFields, request.POST)
    takeCustomDemographicForm = TakeCustomDemographicForm(getCustomDemographicFields(survey), request.POST)


    if request.method == 'POST':
        if takeSurveyForm.is_valid() and takeCustomDemographicForm.is_valid():
            data = takeSurveyForm.cleaned_data
            demographicData = takeCustomDemographicForm.cleaned_data

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

            for field in demographicData:
                fieldID = field[-2:]

                try:
                    fieldID = int(fieldID)
                except ValueError:
                    fieldID = int(fieldID[-1])

                customDemographic = CustomDemographic(userID = request.user,
                                                      demographicField = CustomDemographicField.objects.get(id = fieldID),
                                                      response = demographicData[field])

                customDemographic.save()

            return redirect('index')

        else:
            raise RuntimeError('Invalid form, please try again')


    context = {'request': request, 'takeSurveyForm': takeSurveyForm, 'survey': survey, 'surveyFields': surveyFields, 'takeCustomDemographicForm': takeCustomDemographicForm}

    return renderPage(template, context, request)

class SurveyDelete(DeleteView):
    model = Survey
    success_url = reverse_lazy('surveys')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def view_survey_self_response(request, survey_id):
    if not (isAuthenticated(request.user) and not isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/subject-view-survey-response.html')

    survey = getSurvey(survey_id)
    completedSurvey = getSurveyResponse(request.user, survey)
    completedSurveyDemographics = getCustomDemographicResponse(request.user, survey)

    context = {'request': request, 'survey': survey, 'completedSurvey': completedSurvey, 'completedSurveyDemographics': completedSurveyDemographics}

    return renderPage(template, context, request)

def researcher_invite (request, subject_id):
    if not (isAuthenticated(request.user) and isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/researcher-invite.html')

    user = User.objects.get(id = subject_id)

    researcherInvites = []

    # HACKY FIX FOR REMOVING SURVEYS THAT A SUBJECT ALREADY HAS ACCESS TO. FIX LATER
    for survey in getResearcherInvite(request.user):
        try:
            SurveyAccess.objects.get(surveyID = Survey.objects.get(id = survey.id), userID = user)
        except:
            researcherInvites.append(survey)

    if request.method == 'POST':
        some_var = request.POST.getlist('checks')

        for name in some_var:
            subjectInvite = SurveyAccess(surveyID = Survey.objects.get(id = name),
                                         userID = User.objects.get(id = user.id ))
            subjectInvite.save()
        return redirect('index')

    context = {'request': request, 'userid':user, 'researcherInvite': researcherInvites}

    return renderPage(template, context, request)

def researcher_view_results(request, survey_id):
    if not (isAuthenticated(request.user) and isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/researcher_view_results.html')

    survey = getSurvey(survey_id)
    surveyParticipants = getSurveyTakers(survey)
    participantResults = {}

    for participant in surveyParticipants:
        participantResults[participant] = (getSurveyResponse(participant, survey))
        participantResults[participant] = {'surveyResponse': getSurveyResponse(participant, survey), 'surveyDemographics': getCustomDemographicResponse(participant, survey)}

    context = {'request': request, 'survey': survey, 'participantResults': participantResults}

    return renderPage(template, context, request)

def irb_consent_form(request, survey_id):
    if not (isAuthenticated(request.user) and not isResearcher(request.session)):
        return redirect('index')

    template = setTemplate('QTSurvey/irb-consent.html')
    survey = getSurvey(survey_id)

    if not hasAccess(request.user, survey):
        return redirect('index')

    if hasGivenIRBConsent(request.user, survey):
        return redirect('/takesurvey/{}'.format(survey_id))

    if request.method == 'POST':
        consent = IRBConsent(surveyID = survey, userID = request.user)
        consent.save()

        return redirect('/takesurvey/{}'.format(survey_id))

    context = {'request': request, 'survey': survey}

    return renderPage(template, context, request)

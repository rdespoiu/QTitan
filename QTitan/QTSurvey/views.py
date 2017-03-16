import os
import mimetypes

# Django Imports
from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponse
from django.core.files import File

# Models
from .models import *

# Controllers
from .Controllers import *

# Templates
from .templates import *

# chartit
from chartit import PivotDataPool, PivotChart

#################
# GENERIC VIEWS #
#################

# Index is a redirector
def index(request):
    if isAuthenticated(request.user):
        setResearcher(request)
        return redirect('surveys')

    return redirect('login')

# Registration
def register(request):
    if isAuthenticated(request.user):
        return redirect('index')

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

    return renderPage(REGISTRATION_PAGE, context, request)

# Surveys
def surveys(request):
    if not isAuthenticated(request.user):
        return redirect('index')

    context = {'request': request}

    if isResearcher(request):
        template = RESEARCHER_SURVEYS
        context['researcherSurveys'] = getResearcherSurveys(request)
    else:
        template = SUBJECT_AVAILABLE_SURVEYS
        context['subjectAvailableSurveys'] = getSubjectAvailableSurveys(request)

    return renderPage(template, context, request)


####################
# RESEARCHER VIEWS #
####################

# Subjects
def researcher_subjects(request):
    if not isResearcher(request):
        return redirect('index')

    context = {'request': request, 'researcherSubjects': getResearcherSubjects(request)}

    return renderPage(RESEARCHER_SUBJECTS, context, request)

# Create Survey
def create_survey(request):
    if not isResearcher(request):
        return redirect('index')

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

    return renderPage(CREATE_SURVEY, context, request)

# View aggregate results
def researcher_view_results(request, survey_id):
    if not isResearcher(request):
        return redirect('index')

    survey = getSurvey(survey_id)
    surveyParticipants = getSurveyTakers(survey)
    participantResults = {}

    for participant in surveyParticipants:
        participantResults[participant] = (getSurveyResponse(participant, survey))
        participantResults[participant] = {'surveyResponse': getSurveyResponse(participant, survey), 'surveyDemographics': getCustomDemographicResponse(participant, survey)}

    if not surveyParticipants:
        return redirect('index')

    context = {'request': request, 'survey': survey, 'participantResults': participantResults, 'filename': resultsToCSV(survey, participantResults)}

    return renderPage(RESEARCHER_SURVEY_RESPONSES, context, request)

# View survey analytics
def researcher_survey_analytics(request, survey_id):
	if not isResearcher(request):
		return redirect('index')

	survey = getSurvey(survey_id)
	surveyParticipants = getSurveyTakers(survey)
	participantResults = {}

	for participant in surveyParticipants:
		participantResults[participant] = (getSurveyResponse(participant, survey))
		participantResults[participant] = {'surveyResponse': getSurveyResponse(participant, survey), 'surveyDemographics': getCustomDemographicResponse(participant, survey)}


	context = {'request': request, 'survey': survey, 'participantResults': participantResults}

	return renderPage(RESEARCHER_SURVEY_ANALYTICS, context, request)

# Survey invite
def researcher_invite(request, subject_id):
    if not isResearcher(request):
        return redirect('index')

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

    return renderPage(RESEARCHER_INVITE, context, request)

# Download file
def download(request, filename):
    # Get file path
    filepath = '{}/QTSurvey/SurveyResultCSV/{}'.format(os.path.realpath(''), filename)

    # Open the file
    f = open(filepath, 'r')

    # Set Django File wrapper
    downloadable = File(f)

    # Guess mimetype of file
    filemimetype = mimetypes.guess_type(filepath)

    # Set HttpResponse
    response = HttpResponse(downloadable, content_type=filemimetype)

    # Response header => downloadable
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    # Close the file
    f.close()

    return response


#################
# SUBJECT VIEWS #
#################

# Completed Surveys
def subject_completed_surveys(request):
    if not isSubject(request):
        return redirect('index')

    context = {'request': request, 'subjectCompletedSurveys': getSubjectCompletedSurveys(request)}

    return renderPage(SUBJECT_COMPLETED_SURVEYS, context, request)

# Take Survey
def take_survey(request, survey_id):
    if not isSubject(request):
        return redirect('index')

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
                # Convert ampersand from html to valid string: &amp; => &
                parsedField = field.replace('&amp;', '&')

                completedSurveyField = CompletedSurvey(surveyID = survey,
                                                       surveyFieldID = SurveyField.objects.get(value = parsedField, surveyID = survey),
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

    return renderPage(TAKE_SURVEY, context, request)

# View self response
def view_survey_self_response(request, survey_id):
    if not isSubject(request):
        return redirect('index')

    survey = getSurvey(survey_id)
    completedSurvey = getSurveyResponse(request.user, survey)
    completedSurveyDemographics = getCustomDemographicResponse(request.user, survey)

    context = {'request': request, 'survey': survey, 'completedSurvey': completedSurvey, 'completedSurveyDemographics': completedSurveyDemographics}

    return renderPage(SUBJECT_SURVEY_SELF_RESPONSE, context, request)

# IRB Consent
def irb_consent_form(request, survey_id):
    if not isSubject(request):
        return redirect('index')

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

    return renderPage(IRB_CONSENT, context, request)

# Profile
def profile_view(request,profile_user):
    if not isAuthenticated(request.user):
        return redirect('index')
    
    profileview = getProfileView(profile_user)
    context = {'request':request, 'profileview': profileview}
    return renderPage(PROFILE_PAGE, context, request)

# Preview Survey                                                                                                                                                
def preview_survey(request, survey_id):

    survey = Survey.objects.get(id = survey_id)

    if survey.distribution and not hasAccess(request.user, survey):
        return redirect('index')

    surveyFields = getSurveyFields(survey)
    context = {'request': request, 'survey': survey, 'surveyFields': surveyFields}
    
    return renderPage(PREVIEW_SURVEY, context, request)


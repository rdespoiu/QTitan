# Django Imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

class TestUser:
    firstname = 'FName'
    lastname = 'LName'
    email = 'fnamelname@email.com'
    rsflag = True

'''
def checkForSession()
This method can be used to check whether a user is currently logged in, and redirect appropriately if attempting to access unauthorized views (such as login/register if logged in, or others if not logged in)
Implement this
'''

def testContext():
    loggedInUser = TestUser()
    return {'loggedInUser': loggedInUser}

# Views

# Index only redirects. If there is no user session, redirect to login page.
# If there IS a session, redirect to 'surveys'
def index(request):
    context = testContext()

    if not context['loggedInUser']:
        return redirect('login')
    else:
        return redirect('surveys')

# Registration
def register(request):
    loggedInUser = TestUser()
    loggedInUser = None

    template = loader.get_template('QTSurvey/register.html')
    return HttpResponse(template.render(request))

def login(request):
    template = loader.get_template('QTSurvey/login.html')
    return HttpResponse(template.render(request))

def surveys(request):
    context = testContext()

    if not context['loggedInUser']: return redirect('login')

    if context['loggedInUser'].rsflag:
        template = loader.get_template('QTSurvey/researcher-surveys.html')
    else:
        template = loader.get_template('QTSurvey/subject-available-surveys.html')

    return HttpResponse(template.render(context, request))

def researcher_analytics(request):
    context = testContext()

    if not context['loggedInUser']: return redirect('login')

    template = loader.get_template('QTSurvey/researcher-analytics.html')

    return HttpResponse(template.render(context, request))

def researcher_subjects(request):
    context = testContext()

    if not context['loggedInUser']: return redirect('login')

    template = loader.get_template('QTSurvey/researcher-subjects.html')

    return HttpResponse(template.render(context, request))

def subject_completed_surveys(request):
    context = testContext()

    if not context['loggedInUser']: return redirect('login')

    template = loader.get_template('QTSurvey/subject-completed-surveys.html')

    return HttpResponse(template.render(context, request))

def create_survey(request):
    context = testContext()

    if not context['loggedInUser']: return redirect('login')

    template = loader.get_template('QTSurvey/create-survey.html')

    return HttpResponse(template.render(context, request))

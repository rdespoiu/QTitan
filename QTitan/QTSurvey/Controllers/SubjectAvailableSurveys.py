from .models import *
from itertools import chain

def getSubjectAvailableSurveys(request):
    accessRestrictedSurveys = Survey.objects.filter(id__in = SurveyAccess.objects.filter(userID = request.user))
    openSurveys = Survey.objects.filter(distribution = False)
    completedSurveys = CompletedSurvey.objects.filter(userID = request.user)

    return [survey for survey in chain(accessRestrictedSurveys, openSurveys) if survey not in completedSurveys]

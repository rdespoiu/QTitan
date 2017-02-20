from ..models import *

def getSurvey(surveyID):
    return Survey.objects.get(id = surveyID)

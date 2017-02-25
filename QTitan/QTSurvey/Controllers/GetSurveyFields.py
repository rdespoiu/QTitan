from ..models import *

def getSurveyFields(surveyID):
    return SurveyField.objects.filter(surveyID = surveyID)

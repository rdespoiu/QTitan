from ..models import *

def getCustomDemographicFields(surveyID):
    return CustomDemographicField.objects.filter(surveyID = surveyID)

from ..models import *

def getSurveyTakers(survey):
    return [User.objects.get(id = user[0]) for user in CompletedSurvey.objects.filter(surveyID = survey).values_list('userID').distinct()]

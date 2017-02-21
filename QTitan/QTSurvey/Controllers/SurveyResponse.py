from ..models import *

def getSurveyResponse(userID, survey):
    completedSurvey = sorted(list(CompletedSurvey.objects.filter(surveyID = survey,
                                                                 userID = userID)),
                             key = lambda x: x.orderPosition)
    return completedSurvey

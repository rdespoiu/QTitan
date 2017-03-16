from ..models import CompletedSurvey

sortResultsByOrderPosition = lambda responses: sorted(responses, key = lambda x: x.orderPosition)
getSortedUserResponsesList = lambda survey, participant: sortResultsByOrderPosition(list(CompletedSurvey.objects.filter(surveyID = survey,
                                                                                                                        userID = participant)))

def getAnalyticsData(survey):
    # Hash set of survey participants
    participants = { row.userID for row in CompletedSurvey.objects.filter(surveyID = survey) }

    # Hash table with participants as keys and a sorted list (sorted by orderPosition) of participants' response to the survey
    return { participant: getSortedUserResponsesList(survey, participant) for participant in participants }

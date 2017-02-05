from ..models import *

def getSubjectCompletedSurveys(request):
    query = '''SELECT * FROM QTSurvey_Survey
               WHERE
                id IN (SELECT DISTINCT SurveyID_ID FROM QTSurvey_CompletedSurvey WHERE UserID_ID = {})
            '''.format(request.user.id)

    return list(Survey.objects.raw(query))

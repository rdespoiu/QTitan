from ..models import *

def getSubjectAvailableSurveys(request):
    query = '''SELECT * FROM QTSurvey_Survey
               WHERE
                 (distribution = 0 or
                 id in (SELECT SurveyID_ID FROM QTSurvey_SurveyAccess WHERE UserID_ID = {})) and
                 id not in (SELECT distinct SurveyID_ID from QTSurvey_CompletedSurvey WHERE UserID_ID = {})
                 '''.format(request.user.id, request.user.id)

    return list(Survey.objects.raw(query))

from ..models import *

def getResearcherSurveys(request):
    query = '''
                SELECT   QTSurvey_Survey.ID,
                         QTSurvey_Survey.description,
                         QTSurvey_Survey.distribution,
                         QTSurvey_Survey.OwnerID_ID as owner_id,
                         COUNT(DISTINCT QTSurvey_CompletedSurvey.UserID_ID) as participants

                FROM     QTSurvey_Survey LEFT OUTER JOIN QTSurvey_CompletedSurvey

                ON       QTSurvey_Survey.ID = QTSurvey_CompletedSurvey.SurveyID_ID and QTSurvey_Survey.OwnerID_ID = {}

                GROUP BY QTSurvey_Survey.ID
            '''.format(request.user.id)

    return list(Survey.objects.raw(query))

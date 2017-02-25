from ..models import *

def getCustomDemographicResponse(user, survey):
    query = '''
                SELECT   QTSurvey_CustomDemographic.ID,
                         QTSurvey_CustomDemographic.Response,
                         QTSurvey_CustomDemographicField.Value

                FROM     QTSurvey_CustomDemographic LEFT OUTER JOIN QTSurvey_CustomDemographicField

                ON       QTSurvey_CustomDemographic.DemographicField_ID = QTSurvey_CustomDemographicField.ID

                WHERE    QTSurvey_CustomDemographic.UserID_ID = {} AND
                         QTSurvey_CustomDemographicField.SurveyID_ID = {}

                GROUP BY QTSurvey_CustomDemographic.ID
            '''.format(user.id, survey.id)

    return list(CustomDemographic.objects.raw(query))

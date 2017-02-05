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


'''

select qtsurvey_survey.id, qtsurvey_survey.title, qtsurvey_survey.description, qtsurvey_survey.distribution, qtsurvey_survey.ownerid_id, count(distinct qtsurvey_completedsurvey.userid_id)
from qtsurvey_survey inner join qtsurvey_completedsurvey
on qtsurvey_survey.id = qtsurvey_completedsurvey.surveyid_id and qtsurvey_survey.ownerid_id = 5
group by qtsurvey_survey

select qtsurvey_survey.id, qtsurvey_survey.title, qtsurvey_survey.description, qtsurvey_survey.distribution, qtsurvey_survey.ownerid_id, count(distinct qtsurvey_completedsurvey.userid_id)
from qtsurvey_survey left outer join qtsurvey_completedsurvey
on qtsurvey_survey.id = qtsurvey_completedsurvey.surveyid_id and qtsurvey_survey.ownerid_id = 5
group by qtsurvey_survey.id

select 	qtsurvey_survey.id,
			qtsurvey_survey.title,
			qtsurvey_survey.description,
			qtsurvey_survey.distribution,
			qtsurvey_survey.ownerid_id,
			count(distinct qtsurvey_completedsurvey.userid_id)
from qtsurvey_survey left outer join qtsurvey_completedsurvey
on qtsurvey_survey.id = qtsurvey_completedsurvey.surveyid_id and qtsurvey_survey.ownerid_id = 5
group by qtsurvey_survey.id
'''

from ..models import *

def deleteResearcherSurveys(surveyID):

    survey = '''
                DELETE FROM QTSurvey_Survey
                WHERE ID = {}
             '''.format(surveyID)

    

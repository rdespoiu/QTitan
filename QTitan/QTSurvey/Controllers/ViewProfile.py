from ..models import *

def getProfileView(user):
    query = '''
            Select
                au.id, au.first_name, au.last_name, au.username, au.email, bsd.phone, bsd.dob, csdf.value, csd.response
            From
                QTSurvey_basedemographic bsd Left Join QTSurvey_customdemographic csd on bsd.userID_id= csd.userID_id
                Left Join QTSurvey_customdemographicfield csdf on csd.demographicField_id = csdf.id
                Inner Join auth_user au on bsd.userID_id = au.id
    
            Where 
                au.id = {}
            '''.format(user)

    return list(User.objects.raw(query))
from ..models import Survey, SurveyAccess

def hasAccess(user, survey):
    if Survey.objects.get(id = survey.id).distribution:
        try:
            SurveyAccess.objects.get(surveyID = survey, userID = user)
        except:
            return False
    return True

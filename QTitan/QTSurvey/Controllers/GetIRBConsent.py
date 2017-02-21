from ..models import IRBConsent

def hasGivenIRBConsent(user, survey):
    try:
        IRBConsent.objects.get(surveyID = survey, userID = user)
        return True
    except:
        return False

from ..models import *

def deleteResearcherSurveys(request):
   query = '''DELETE FROM QTSurvey_Survey
              WHERE
              ownerID=? LIMIT 1
              UPDATE Survey
            '''.format(request.user.id)

    return list(Survey.objects.raw(query))




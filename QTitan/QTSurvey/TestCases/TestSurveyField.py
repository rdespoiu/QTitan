from django.test import TestCase
from ..models import Survey, SurveyField, User

class SurveyFieldTestCase(TestCase):
    def setUp(self):
        self.TEST_USER = User.objects.create(username = 'TestUser',
                                             password = 'TestPassword',
                                             first_name = 'TestFirstName',
                                             last_name = 'TestLastName',
                                             email = 'Test@email.com')

        self.TEST_SURVEY = Survey.objects.create(ownerID = self.TEST_USER,
                                                 title = 'SurveyTestTitle',
                                                 description = 'SurveyTestDescription',
                                                 distribution = True,
                                                 consentneeded = True)

        SurveyField.objects.create(surveyID = self.TEST_SURVEY,
                                   value = 'TestValue1')

        SurveyField.objects.create(surveyID = self.TEST_SURVEY,
                                   value = 'TestValue2')

        SurveyField.objects.create(surveyID = self.TEST_SURVEY,
                                   value = 'TestValue3')

    def testSurveyFieldObject(self):
        TEST_SURVEY_FIELDS = sorted(list(SurveyField.objects.filter(surveyID = self.TEST_SURVEY)), key = lambda field: field.value)

        for i in range(len(TEST_SURVEY_FIELDS)):
            self.assertEqual(TEST_SURVEY_FIELDS[i].surveyID, self.TEST_SURVEY)
            self.assertEqual(TEST_SURVEY_FIELDS[i].value, 'TestValue{}'.format(i + 1))

from django.test import TestCase
from ..models import Survey, SurveyField, CompletedSurvey, User

class CompletedSurveyTestCase(TestCase):
    def setUp(self):
        self.TEST_USER = User.objects.create(username = 'TestUser',
                                             password = 'TestPassword',
                                             first_name = 'TestFirstName',
                                             last_name = 'TestLastName',
                                             email = 'Test@email.com')

        self.TEST_USER2 = User.objects.create(username = 'TestUser2',
                                              password = 'TestPassword2',
                                              first_name = 'TestFirstName2',
                                              last_name = 'TestLastName2',
                                              email = 'Test2@email.com')

        self.TEST_SURVEY = Survey.objects.create(ownerID = self.TEST_USER,
                                                 title = 'SurveyTestTitle',
                                                 description = 'SurveyTestDescription',
                                                 distribution = True,
                                                 consentneeded = True)

        self.TEST_SF1 = SurveyField.objects.create(surveyID = self.TEST_SURVEY,
                                                   value = 'TestValue1')

        self.TEST_SF2 = SurveyField.objects.create(surveyID = self.TEST_SURVEY,
                                                   value = 'TestValue2')

        self.TEST_SF3 = SurveyField.objects.create(surveyID = self.TEST_SURVEY,
                                                   value = 'TestValue3')

        CompletedSurvey.objects.create(surveyID = self.TEST_SURVEY,
                                       surveyFieldID = self.TEST_SF1,
                                       userID = self.TEST_USER2,
                                       orderPosition = 1)

        CompletedSurvey.objects.create(surveyID = self.TEST_SURVEY,
                                       surveyFieldID = self.TEST_SF2,
                                       userID = self.TEST_USER2,
                                       orderPosition = 2)

        CompletedSurvey.objects.create(surveyID = self.TEST_SURVEY,
                                       surveyFieldID = self.TEST_SF3,
                                       userID = self.TEST_USER2,
                                       orderPosition = 3)

    def testCompletedSurveyObject(self):
        TEST_COMPLETED_SURVEYS = sorted(list(CompletedSurvey.objects.filter(surveyID = self.TEST_SURVEY, userID = self.TEST_USER2)), key = lambda survey: survey.orderPosition)

        for i in range(len(TEST_COMPLETED_SURVEYS)):
            self.assertEqual(TEST_COMPLETED_SURVEYS[i].surveyID, self.TEST_SURVEY)
            self.assertEqual(TEST_COMPLETED_SURVEYS[i].userID, self.TEST_USER2)
            self.assertEqual(TEST_COMPLETED_SURVEYS[i].orderPosition, i + 1)
            self.assertEqual(TEST_COMPLETED_SURVEYS[i].surveyFieldID, SurveyField.objects.get(value = 'TestValue{}'.format(i + 1)))

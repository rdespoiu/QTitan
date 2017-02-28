from django.test import TestCase
from ..models import Survey, SurveyAccess, User

class SurveyAccessTestCase(TestCase):
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

        SurveyAccess.objects.create(surveyID = self.TEST_SURVEY,
                                    userID = self.TEST_USER2)

    def testSurveyAccessObject(self):
        TEST_SURVEY_ACCESS = SurveyAccess.objects.get(surveyID = self.TEST_SURVEY, userID = self.TEST_USER2)

        self.assertEqual(TEST_SURVEY_ACCESS.surveyID, self.TEST_SURVEY)
        self.assertEqual(TEST_SURVEY_ACCESS.userID, self.TEST_USER2)

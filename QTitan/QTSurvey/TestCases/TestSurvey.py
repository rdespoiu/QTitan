from django.test import TestCase
from ..models import Survey, User

class SurveyTestCase(TestCase):
    def setUp(self):
        self.TEST_USER = User.objects.create(username = 'TestUser',
                                             password = 'TestPassword',
                                             first_name = 'TestFirstName',
                                             last_name = 'TestLastName',
                                             email = 'Test@email.com')

        Survey.objects.create(ownerID = self.TEST_USER,
                              title = 'SurveyTestTitle',
                              description = 'SurveyTestDescription',
                              distribution = True,
                              consentneeded = True)

    def testSurveyObject(self):
        TEST_SURVEY = Survey.objects.get(ownerID = self.TEST_USER)

        self.assertEqual(TEST_SURVEY.ownerID, self.TEST_USER)
        self.assertEqual(TEST_SURVEY.title, 'SurveyTestTitle')
        self.assertEqual(TEST_SURVEY.description, 'SurveyTestDescription')
        self.assertEqual(TEST_SURVEY.distribution, True)
        self.assertEqual(TEST_SURVEY.consentneeded, True)

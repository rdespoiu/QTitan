from django.test import TestCase
from ..models import Survey, User, IRBConsent

class IRBConsentTestCase(TestCase):
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

        IRBConsent.objects.create(surveyID = self.TEST_SURVEY,
                                  userID = self.TEST_USER2)

    def testIRBConsentObject(self):
        TEST_IRB_CONSENT = IRBConsent.objects.get(surveyID = self.TEST_SURVEY, userID = self.TEST_USER2)

        self.assertEqual(TEST_IRB_CONSENT.surveyID, self.TEST_SURVEY)
        self.assertEqual(TEST_IRB_CONSENT.userID, self.TEST_USER2)

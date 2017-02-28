from django.test import TestCase
from ..models import CustomDemographic, CustomDemographicField, Survey, User

class CustomDemographicTestCase(TestCase):
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

        self.TEST_CDF1 = CustomDemographicField.objects.create(surveyID = self.TEST_SURVEY,
                                                               value = 'CustomDemographicField1')

        self.TEST_CDF2 = CustomDemographicField.objects.create(surveyID = self.TEST_SURVEY,
                                                               value = 'CustomDemographicField2')

        self.TEST_CDF3 = CustomDemographicField.objects.create(surveyID = self.TEST_SURVEY,
                                                               value = 'CustomDemographicField3')

        CustomDemographic.objects.create(userID = self.TEST_USER2,
                                         demographicField = self.TEST_CDF1,
                                         response = 'CustomDemographicResponse1')

        CustomDemographic.objects.create(userID = self.TEST_USER2,
                                         demographicField = self.TEST_CDF2,
                                         response = 'CustomDemographicResponse2')

        CustomDemographic.objects.create(userID = self.TEST_USER2,
                                         demographicField = self.TEST_CDF3,
                                         response = 'CustomDemographicResponse3')

    def testCustomDemographicObject(self):
        TEST_CUSTOM_DEMOGRAPHIC = sorted(list(CustomDemographic.objects.filter(userID = self.TEST_USER2)), key = lambda demo: demo.response)

        for i in range(len(TEST_CUSTOM_DEMOGRAPHIC)):
            self.assertEqual(TEST_CUSTOM_DEMOGRAPHIC[i].userID, self.TEST_USER2)
            self.assertEqual(TEST_CUSTOM_DEMOGRAPHIC[i].demographicField, CustomDemographicField.objects.get(value = 'CustomDemographicField{}'.format(i + 1)))
            self.assertEqual(TEST_CUSTOM_DEMOGRAPHIC[i].response, 'CustomDemographicResponse{}'.format(i + 1))

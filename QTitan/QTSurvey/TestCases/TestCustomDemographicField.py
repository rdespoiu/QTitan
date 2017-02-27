from django.test import TestCase
from ..models import CustomDemographicField, Survey, User

class CustomDemographicFieldTestCase(TestCase):
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

        CustomDemographicField.objects.create(surveyID = self.TEST_SURVEY,
                                              value = 'CustomDemographicField1')

        CustomDemographicField.objects.create(surveyID = self.TEST_SURVEY,
                                              value = 'CustomDemographicField2')

        CustomDemographicField.objects.create(surveyID = self.TEST_SURVEY,
                                              value = 'CustomDemographicField3')

    def testCustomDemographicFieldObject(self):
        TEST_CUSTOM_DEMOGRAPHIC_FIELD = sorted(list(CustomDemographicField.objects.filter(surveyID = self.TEST_SURVEY)), key = lambda field: field.value)

        for i in range(len(TEST_CUSTOM_DEMOGRAPHIC_FIELD)):
            self.assertEqual(TEST_CUSTOM_DEMOGRAPHIC_FIELD[i].surveyID, self.TEST_SURVEY)
            self.assertEqual(TEST_CUSTOM_DEMOGRAPHIC_FIELD[i].value, 'CustomDemographicField{}'.format(i + 1))

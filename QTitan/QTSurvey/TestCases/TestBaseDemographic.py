from django.test import TestCase
from ..models import BaseDemographic, User
from datetime import datetime

class BaseDemographicTestCase(TestCase):
    TEST_DOB = datetime(2017,2,27)

    def setUp(self):
        self.TEST_USER = User.objects.create(username = 'TestUser',
                                             password = 'TestPassword',
                                             first_name = 'TestFirstName',
                                             last_name = 'TestLastName',
                                             email = 'Test@email.com')

        BaseDemographic.objects.create(userID = self.TEST_USER,
                                       first_name = self.TEST_USER.first_name,
                                       last_name = self.TEST_USER.last_name,
                                       phone = '5555555555',
                                       dob = self.TEST_DOB)

    def testBaseDemographicObject(self):
        TEST_BASE_DEMOGRAPHIC = BaseDemographic.objects.get(userID = self.TEST_USER)

        self.assertEqual(TEST_BASE_DEMOGRAPHIC.userID, self.TEST_USER)
        self.assertEqual(TEST_BASE_DEMOGRAPHIC.first_name, 'TestFirstName')
        self.assertEqual(TEST_BASE_DEMOGRAPHIC.last_name, 'TestLastName')
        self.assertEqual(TEST_BASE_DEMOGRAPHIC.phone, '5555555555')
        self.assertEqual(TEST_BASE_DEMOGRAPHIC.dob.year, self.TEST_DOB.year)
        self.assertEqual(TEST_BASE_DEMOGRAPHIC.dob.month, self.TEST_DOB.month)
        self.assertEqual(TEST_BASE_DEMOGRAPHIC.dob.day, self.TEST_DOB.day)

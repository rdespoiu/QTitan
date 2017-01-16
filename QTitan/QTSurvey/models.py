# Django Imports
from django.db import models

#############
# DB Models #
#############

# Users
# RSFlag designates researcher. False by default, so when users register they will automatically be subjects. Researchers are manually added
class User(models.Model):
    RSFlag = models.BooleanField(default = False)
    email = models.CharField(max_length = 80)
    password = models.CharField(max_length = 128)
    salt = models.CharField(max_length = 128)

# Demographics common to all users (researchers/subjects)
class BaseDemographic(models.Model):
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    firstName = models.CharField(max_length = 40)
    lastName = models.CharField(max_length = 40)
    phone = models.CharField(max_length = 11)
    dob = models.DateField()

# Custom demographics that some researchers may require subjects to populate
class CustomDemographic(models.Model):
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    field = models.CharField(max_length = 40)
    value = models.CharField(max_length = 40)

# Survey
# Distribution indicates whether a survey is open to all or by invite only. Default False = invite only
class Survey(models.Model):
    ownerID = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 256)
    description = models.CharField(max_length = 512)
    distribution = models.BooleanField(default = False)

# Survey option
class SurveyField(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    value = models.CharField(max_length = 256)

# Completed surveys. orderPosition designates in which order each SurveyField was placed
class CompletedSurvey(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    surveyFieldID = models.ForeignKey(SurveyField, on_delete = models.CASCADE)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    orderPosition = models.IntegerField()

# For survey distribution, to check whether a subject has access to a survey.
class SurveyAccess(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)

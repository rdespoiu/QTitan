# Django Imports
import django
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from pickle import TRUE
from django.template.defaultfilters import default

#############
# DB Models #
#############

# Demographics common to all users (researchers/subjects)
class BaseDemographic(models.Model):
    demoId = models.IntegerField(primary_key = True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    first_name= models.CharField(max_length = 40, null = True)
    last_name = models.CharField(max_length = 40, null = True)
    phone = models.CharField(max_length = 11, null = TRUE)
    dob = models.DateField( null= True)

# Survey
# Distribution indicates whether a survey is open to all or by invite only. Default False = invite only
class Survey(models.Model):
    ownerID = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 256)
    description = models.CharField(max_length = 512)
    distribution = models.BooleanField(default = False)
    consentneeded = models.BooleanField(default = False)

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

# Custom demographic field
class CustomDemographicField(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    value = models.CharField(max_length = 256)

# Custom demographic object
class CustomDemographic(models.Model):
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    demographicField = models.ForeignKey(CustomDemographicField, on_delete = models.CASCADE)
    response = models.CharField(max_length = 256)

# For survey distribution, to check whether a subject has access to a survey.
class SurveyAccess(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)

# IRB Consent
class IRBConsent(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)

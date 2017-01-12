# Django Imports
from django.db import models

#############
# DB Models #
#############

# Researchers
class User(models.Model):
    email = models.CharField(max_length = 80)
    firstName = models.CharField(max_length = 40)
    lastName = models.CharField(max_length = 40)
    phone = models.CharField(max_length = 11)
    password = models.CharField(max_length = 128)
    salt = models.CharField(max_length = 32)

# Subjects
class Subject(models.Model):
    researcherID = models.ForeignKey(User, on_delete = models.CASCADE)
    firstName = models.CharField(max_length = 40)
    lastName = models.CharField(max_length = 40)
    email = models.CharField(max_length = 80)
    phone = models.CharField(max_length = 11)

# Additional subject demographic information if researchers need it
class CustomDemographic(models.Model):
    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE)
    title = models.CharField(max_length = 60)
    description = models.CharField(max_length = 60)

# Surveys
class Survey(models.Model):
    ownerID = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    distribution = models.BooleanField(default = False)

# Questions in surveys
class Question(models.Model):
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)

# Subject responses to surveys
class SurveyResponse(models.Model):
    questionID = models.ForeignKey(Question, on_delete = models.CASCADE)
    surveyID = models.ForeignKey(Survey, on_delete = models.CASCADE)
    subjectID = models.ForeignKey(Subject, on_delete = models.CASCADE)
    respone = models.CharField(max_length = 500)

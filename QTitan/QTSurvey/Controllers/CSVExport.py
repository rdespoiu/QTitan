from ..models import *
from datetime import date
from hashlib import sha224

# Lambda method to calculate age from data.today() - dob
calculateAge = lambda dob, today: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))



def resultsToCSV(survey, participantResults):
    csvData = populateCSVData(survey, participantResults)
    return writeToFile(survey, csvData)

def populateCSVData(survey, participantResults):
    today = date.today()

    csvData = {
        'SurveyHeader': 'Survey\nSurveyID,Owner ID,Owner Username,Survey Title,Survey Description,Distribution,Consent',
        'SurveyDetail': '{},{},{},{},{},{},{}'.format(survey.id,
                                                      survey.ownerID.id,
                                                      survey.ownerID.username,
                                                      survey.title,
                                                      survey.description,
                                                      survey.distribution,
                                                      survey.consentneeded),

        'SurveyTakersHeader': 'SurveyTakers\nUser ID,Username,First Name,Last Name,Date of Birth,Age,Email',
        'SurveyTakersDetail': [],

        'SurveyResponsesHeader': 'Survey Responses\nUser ID,Username,Survey Field,Order Position',
        'SurveyResponsesDetail': [],

        'DemographicsHeader': 'Survey Demographics\nUser ID,Username,Demographic Field,Response',
        'DemographicsDetail': []
    }


    for participant in participantResults:
        # Get DOB
        participantDOB = BaseDemographic.objects.get(userID = participant.id).dob

        # Add data for each survey taker
        csvData['SurveyTakersDetail'].append('{},{},{},{},{},{},{}'.format(participant.id,
                                                                           participant.username,
                                                                           participant.first_name,
                                                                           participant.last_name,
                                                                           participantDOB,
                                                                           calculateAge(participantDOB, today),
                                                                           participant.email))

        # Add data for each survey response
        for response in participantResults[participant]['surveyResponse']:
            csvData['SurveyResponsesDetail'].append('{},{},{},{}'.format(participant.id,
                                                                         participant.username,
                                                                         response.surveyFieldID.value,
                                                                         response.orderPosition))

        # Add data for each demographic response
        for response in participantResults[participant]['surveyDemographics']:
            csvData['DemographicsDetail'].append('{},{},{},{}'.format(participant.id,
                                                                      participant.username,
                                                                      response.value,
                                                                      response.response))

    return csvData

def writeToFile(survey, csvData):
    # Define filename
    filename = cleanString('{}_{}_{}_{}.csv'.format(survey.ownerID.username, survey.id, survey.title, date.today()))

    # Create (or replace) file
    f = open('QTSurvey/SurveyResultCSV/{}'.format(filename), 'w')

    # Write Survey Header and Details
    f.write('{}\n'.format(csvData['SurveyHeader']))
    f.write('{}\n\n'.format(csvData['SurveyDetail']))

    # Write Survey Takers Header and Details
    f.write('{}\n'.format(csvData['SurveyTakersHeader']))
    for participant in csvData['SurveyTakersDetail']:
        f.write('{}\n'.format(participant))

    # Write Survey Responses Header and Details
    f.write('\n{}\n'.format(csvData['SurveyResponsesHeader']))
    for response in csvData['SurveyResponsesDetail']:
        f.write('{}\n'.format(response))

    # Write Demographics Header and Details
    f.write('\n{}\n'.format(csvData['DemographicsHeader']))
    for response in csvData['DemographicsDetail']:
        f.write('{}\n'.format(response))

    f.close()

    return filename

def cleanString(string):
    return string.replace(' ', '_')

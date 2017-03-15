from .Controllers import setTemplate

#################
# GENERIC VIEWS #
#################

# Registration page
REGISTRATION_PAGE = setTemplate('QTSurvey/register.html')


####################
# RESEARCHER VIEWS #
####################

# Researcher surveys
RESEARCHER_SURVEYS = setTemplate('QTSurvey/researcher-surveys.html')

# Researcher subjects
RESEARCHER_SUBJECTS = setTemplate('QTSurvey/researcher-subjects.html')

# Create survey
CREATE_SURVEY = setTemplate('QTSurvey/create-survey.html')

# Researcher invite
RESEARCHER_INVITE = setTemplate('QTSurvey/researcher-invite.html')

# Researcher survey responses
RESEARCHER_SURVEY_RESPONSES = setTemplate('QTSurvey/researcher_view_results.html')

# Researcher Analytics
RESEARCHER_SURVEY_ANALYTICS = setTemplate('QTSurvey/researcher_survey_analytics.html')

#################
# SUBJECT VIEWS #
#################

# Subject available surveys
SUBJECT_AVAILABLE_SURVEYS = setTemplate('QTSurvey/subject-available-surveys.html')

# Subject completed surveys
SUBJECT_COMPLETED_SURVEYS = setTemplate('QTSurvey/subject-completed-surveys.html')

# Take survey
TAKE_SURVEY = setTemplate('QTSurvey/take-survey.html')

# Subject survey self response
SUBJECT_SURVEY_SELF_RESPONSE = setTemplate('QTSurvey/subject-view-survey-response.html')

# IRB Consent
IRB_CONSENT = setTemplate('QTSurvey/irb-consent.html')

PREVIEW_SURVEY = setTemplate('QTSurvey/preview-survey.html')

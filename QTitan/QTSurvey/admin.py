from django.contrib import admin

from .models import (
    BaseDemographic,
    CustomDemographic,
    CustomDemographicField,
    Survey,
    SurveyField,
    CompletedSurvey,
    SurveyAccess
)

# Model registration
admin.site.register(BaseDemographic)
admin.site.register(CustomDemographic)
admin.site.register(CustomDemographicField)
admin.site.register(Survey)
admin.site.register(SurveyField)
admin.site.register(CompletedSurvey)
admin.site.register(SurveyAccess)

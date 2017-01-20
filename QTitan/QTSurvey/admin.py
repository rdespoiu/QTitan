from django.contrib import admin
from .models import \
                    User,               \
                    BaseDemographic,    \
                    CustomDemographic,  \
                    Survey,             \
                    SurveyField,        \
                    CompletedSurvey,    \
                    SurveyAccess

# Model registration
admin.site.register(User)
admin.site.register(BaseDemographic)
admin.site.register(CustomDemographic)
admin.site.register(Survey)
admin.site.register(SurveyField)
admin.site.register(CompletedSurvey)
admin.site.register(SurveyAccess)

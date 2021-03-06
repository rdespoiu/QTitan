from ..models import *
from datetime import date

# Lambda method to calculate age from data.today() - dob
calculateAge = lambda dob, today: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def getResearcherSubjects(request):
    # Get today's date (for age lambda)
    today = date.today()

    # Query returning all subjects from BaseDemographic
    subjects = BaseDemographic.objects.all()

    for subject in subjects:
        # Add a new age value calculated from DOB
        subject.age = calculateAge(subject.dob, today)
        try:
            subject.email = User.objects.get(id = subject.userID.id).email
        except:
            subject.email = "N/A"

    # Filters out any users that are members of any group
    return list(filter(lambda subject : not len(subject.userID.groups.filter()), subjects))

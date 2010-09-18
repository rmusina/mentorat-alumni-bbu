from django.contrib import admin
from profiles.models import *

admin.site.register(Profile)
admin.site.register(StudentProfile)
admin.site.register(MentorProfile)
admin.site.register(VolunteerOrganization)
admin.site.register(StudentEmployment)
admin.site.register(FieldOfInterest)
admin.site.register(FieldOfInterest_Profile)
admin.site.register(CommunicationMethod)
admin.site.register(CommunicationRating)
admin.site.register(MentorshipActivities)
admin.site.register(MentorshipActivities_Mentor)
admin.site.register(StudentResearch)

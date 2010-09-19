from django.contrib import admin
from profiles.models import *

class VolunteerOrganizationInline(admin.StackedInline):
    model = VolunteerOrganization
    fk_name = 'profile'
    extra = 0

class CommunicationRatingInline(admin.StackedInline):
    model = CommunicationRating
    fk_name = 'profile'
    extra = 0

class FieldOfInterest_ProfileInline(admin.StackedInline):
    model = FieldOfInterest_Profile
    fk_name = 'profile'
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        VolunteerOrganizationInline,
        CommunicationRatingInline,
        FieldOfInterest_ProfileInline,
    ]

class StudentEmploymentInline(admin.StackedInline):
    model = StudentEmployment
    fk_name = 'student'
    extra = 0

class StudentProfileAdmin(admin.ModelAdmin):
    inlines = [
        StudentEmploymentInline,
    ]

class MentorshipActivities_MentorInline(admin.StackedInline):
    model = MentorshipActivities_Mentor
    fk_name = 'mentor'
    extra = 0

class MentorProfileAdmin(admin.ModelAdmin):
    inlines = [
        MentorshipActivities_MentorInline,
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(MentorProfile, MentorProfileAdmin)

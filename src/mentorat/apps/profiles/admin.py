from django.contrib import admin
from profiles.models import Profile, StudentProfile, MentorProfile

admin.site.register(Profile)
admin.site.register(StudentProfile)
admin.site.register(MentorProfile)
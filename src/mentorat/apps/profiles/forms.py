from django import forms
from profiles.models import Profile, StudentProfile, MentorProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ('user')
        
class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        exclude = ('user')
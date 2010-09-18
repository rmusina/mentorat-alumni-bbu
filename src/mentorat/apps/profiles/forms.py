from django import forms
from profiles.models import Profile, StudentProfile, MentorProfile
from django.utils.translation import ugettext_lazy as _

months_with_30 = [4, 6, 9, 11]
def is_valid_cnp(value):
    if not value or len(value) != 13 or not value.isdigit:
        return False
    if value[0] != '1' and value[0] != '2':
        return False
    month = eval(value[3:5])
    day = eval(value[5:7])
    if month < 1 or month > 12 or day < 1 or day > 31:
        return False
    if month in months_with_30 and day == 30:
        return False
    if month == 2 and day > 29:
        return False
    return True

error_messages_charfields = { 'required': _('You must fill in this field'), 'max_length': _('You input is too long, it should be at most %d characters long.'), 
                              'min_length': _('You input is too short, it should be at least %d characters long.') }

class GeneralInfoForm(forms.ModelForm):
    firstname = forms.CharField(label=_('First name'), error_messages=error_messages_charfields, max_length=30)
    surname = forms.CharField(label=_('Surname'), error_messages=error_messages_charfields, max_length=30)
    previous_surname = forms.CharField(label=_('Surname before marriage (is applicable)'), error_messages=error_messages_charfields, 
                                       max_length=30, required=False)
    CNP = forms.CharField(label=_('CNP'), error_messages={'required': _('You must fill in this field'),
                                                          'min_length': _('The CNP is %d digits long'), 
                                                          'max_length': _('The CNP is %d digits long')}, min_length=13, max_length=13)
    age = forms.IntegerField(required=False, label=_('Age (optional)'), 
                             error_messages={'invalid': _('Enter a valid age'), 'max_value': _('Are you really that old? You can\'t be older than %d.'), 'min_value': _('You are too young to be a student. You must be at least %d.')}, 
                             min_value=15, max_value=100)
    email = forms.EmailField(label=_('Email'), error_messages={'required': _('You must fill in this field'), 'invalid': _('This email address is invalid')},
                             max_length=50)
    telephone = forms.CharField(label=_('Telephone'), error_messages=error_messages_charfields,
                                max_length=20)
    address = forms.CharField(label=_('Address'), error_messages=error_messages_charfields,
                              max_length=100, widget=forms.Textarea)

    def clean_CNP(self):
        cnp = str(self.cleaned_data['CNP'])
        if not is_valid_cnp(cnp):
            raise forms.ValidationError(_('Invalid CNP entered'))
        return cnp

    class Meta:
        model = Profile
        exclude = ('user')


# Student profile editing forms
class StudentGeneralInfoForm(GeneralInfoForm):
    birthplace = forms.CharField(label=_('Birth place'), error_messages=error_messages_charfields,
                                 max_length=50)
    faculty = forms.CharField(label=_('Current faculty'), error_messages=error_messages_charfields,
                              max_length=100)
    year_of_study = forms.IntegerField(label=_('Year of study'), error_messages={'invalid': _('Enter a valid year of study'), 'required': _('This field cannot be empty'), 
                                                                                 'min_value': _('The year of study must be at least %d'),
                                                                                 'max_value': _('The year of study can be at most %d')}, 
                                       min_value=1, max_value=6)
    major = forms.CharField(label=_('Major'), error_messages=error_messages_charfields, max_length=100)
    town_of_study = forms.CharField(label=_('Town of study'), error_messages=error_messages_charfields, max_length=50)


    class Meta:
        model = StudentProfile
        fields = [ 'firstname', 'surname', 'previous_surname', 'CNP', 'birthplace', 'age', 'faculty', 'year_of_study', 'major', 'email', 'telephone', 'address', 'town_of_study']


class StudentEmploymentForm(forms.ModelForm):
    employer_name = forms.CharField(required=False, label=_('Employer\'s name (optional)'), max_length=50, error_messages=error_messages_charfields)
    employer_address = forms.CharField(required=False, label=_('Employer\'s address (optional)'), max_length=100, error_messages=error_messages_charfields)
    employee_position = forms.CharField(required=False, label=_('Position held (optional)'), max_length=100, error_messages=error_messages_charfields)
    employee_duties = forms.CharField(widget=forms.Textarea, required=False, label=_('Duties (optional)'))
    class Meta:
        model = StudentProfile
        fields = ['employer_name', 'employer_address', 'employee_position', 'employee_duties']


# mentor profile editing forms    
class MentorGeneralInfoForm(GeneralInfoForm):
    class Meta:
        model = MentorProfile
        exclude = ('user')


class MentorEmploymentForm(forms.ModelForm):
    class Meta:
        model = MentorProfile

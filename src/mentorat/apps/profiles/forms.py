from django import forms
from profiles.models import Profile, StudentProfile, MentorProfile, FieldOfInterest, FieldOfInterest_Profile
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

error_messages_charfields = { 'required': _('You must fill in this field'), 'max_length': _('You input is too long'),
                              'min_length': _('You input is too short') }

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
        

def get_choice_list():
    return [ (x.pk, x.name) for x in FieldOfInterest.objects.all() ]

def get_initial_values(profile):
    return [ x.field.pk for x in profile.fields_of_interest.all() ]
    
    
class StudentProfessionalForm(forms.ModelForm):    
    home_town = forms.CharField(max_length=50, error_messages=error_messages_charfields, label=_('Home town'))
    graduated_college = forms.CharField(max_length=100, widget=forms.Textarea, error_messages=error_messages_charfields,
                                        label=_('Graduated college'))
    future_plans = forms.CharField(widget=forms.Textarea, error_messages=error_messages_charfields,
                                        label=_('Plans for the following year'))
    how_mentor_can_help = forms.CharField(widget=forms.Textarea, error_messages=error_messages_charfields,
                                        label=_('How can a mentor help in the student\'s development?'))
    fields_of_interest = forms.MultipleChoiceField(required=False, label=_('Fields of interest for mentorship (between 1 and 3)'), choices=get_choice_list(), widget=forms.CheckboxSelectMultiple)
    
    def clean_fields_of_interest(self):
        data = self.cleaned_data['fields_of_interest']
        if len(data) < 1:
            raise forms.ValidationError(_('You have to choose at least 1 field of interest'))
        if len(data) > 3:
            raise forms.ValidationError(_('You may choose at most 3 fields of interest'))
        data = [ int(x) for x in data ]
        return data
     
    def __init__(self, *args, **keywords):
        forms.ModelForm.__init__(self, *args, **keywords)
        if len(args)==0 and len(keywords)==1 and 'instance' in keywords:
            self.initial['fields_of_interest'] = get_initial_values(keywords['instance'])     
            
    def save(self, commit=True):
        super(forms.ModelForm, self).save(commit=commit)
        
        fields_of_interest = [ FieldOfInterest.objects.get(pk=x) for x in self.cleaned_data['fields_of_interest'] ]
        for field in fields_of_interest:
            FieldOfInterest_Profile.objects.get_or_create(profile=self.instance, field=field)
        for foi in FieldOfInterest_Profile.objects.filter(profile=self.instance):
            if not foi.field in fields_of_interest:
                foi.delete()
         
        return self.instance
            
    class Meta:
        model = StudentProfile 
        fields = ['home_town', 'graduated_college', 'future_plans', 'fields_of_interest', 'how_mentor_can_help']


class StudentAdditionalForm(forms.ModelForm):
    hobbies = forms.CharField(widget=forms.Textarea, required=False, label=_('What are you hobbies?'), error_messages={'required': _('You must fill in this field')})
    self_evaluation = forms.CharField(widget=forms.Textarea, label=_('How would you describe yourself as a colleague?'), error_messages={'required': _('You must fill in this field')})
    mentor_expectations = forms.CharField(widget=forms.Textarea, label=_('What are you expectations of a mentor?'), error_messages={'required': _('You must fill in this field')})
    extra_info = forms.CharField(widget=forms.Textarea, required=False, label=_('Do you have any additional information you might want to share with a possible mentor?'), error_messages={'required': _('You must fill in this field')})
    # TODO: add communication ratings
    
    class Meta:
        model = StudentProfile
        fields = ['hobbies',  'self_evaluation', 'mentor_expectations', 'extra_info']


# mentor profile editing forms    
class MentorGeneralInfoForm(GeneralInfoForm):
    class Meta:
        model = MentorProfile
        exclude = ('user')


class MentorEmploymentForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
      
        
class MentorProfessionalForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        
        
class MentorAdditionalForm(forms.ModelForm):
    class Meta:
        model = MentorProfile

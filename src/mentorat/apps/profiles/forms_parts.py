from django import forms
from profiles.models import VolunteerOrganization, StudentEmployment, StudentResearch
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

err_msg_char = { 'required': _('This field is required'), 'max_length': _('Your input is too long') }
class VolunteerForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label=_('Organization name'), error_messages=err_msg_char)
    field = forms.CharField(max_length=100, required=False, widget=forms.Textarea, label=_('Field'), error_messages=err_msg_char) 
    
    class Meta:
        model = VolunteerOrganization
        fields = ['name', 'field' ]
        
class EmploymentForm(forms.ModelForm):
    internship = forms.BooleanField(required=False, label=_('Internship'), widget=forms.CheckboxInput)
    employer_name = forms.CharField(max_length=50, label=_('Employer\'s name'), error_messages=err_msg_char)
    position = forms.CharField(max_length=100, label=_('Postion held'))
    duties = forms.CharField(required=False, widget=forms.Textarea, error_messages=err_msg_char, label=_('Duties'))
    start_date = forms.DateField(label=_('Start date (year-month-day)'), error_messages={'required': _('This field is required'), 
                                                                                         'invalid': _('You have entered an invalid date. Enter a date in the format year-month-day.')})
    end_date = forms.DateField(label=_('End date (year-month-day)'), error_messages={'required': _('This field is required'), 
                                                                                     'invalid': _('You have entered an invalid date. Enter a date in the format year-month-day.')})
    
    class Meta:
        model = StudentEmployment
        fields = ['internship', 'employer_name', 'position', 'duties', 'start_date', 'end_date']
        
        
class ResearchForm(forms.ModelForm):
    field = forms.CharField(max_length=100, label=_('Field of research'), error_messages=err_msg_char)
    duties = forms.CharField(widget=forms.Textarea, label=_('Duties'), error_messages=err_msg_char)
    
    class Meta:
        model = StudentResearch
        fields = ['field', 'duties' ]
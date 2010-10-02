from django import forms
from surveys.models import *
from django.utils.translation import ugettext_lazy as _

error_messages_charfields = { 'required': _('This field is required'), 'max_length': _('You input is too long'),
                              'min_length': _('You input is too short') }


class AddSurveyForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=255, label=_('Survey name'), error_messages=error_messages_charfields)
    description = forms.CharField(required=False, widget=forms.Textarea, label=_('Desciption'))
    for_students = forms.BooleanField(initial=True, label=_('Student survey'), required=False)
    for_mentors = forms.BooleanField(initial=False, label=_('Mentor survey'), required=False)

    class Meta:
        model = Survey
    

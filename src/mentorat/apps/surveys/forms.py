from django import forms
from surveys.models import *
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

error_messages_charfields = { 'required': _('This field is required'), 'max_length': _('You input is too long'),
                              'min_length': _('You input is too short') }


class AddSurveyForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=255, label=_('Survey name'), error_messages=error_messages_charfields)
    description = forms.CharField(required=False, widget=forms.Textarea, label=_('Desciption'))
    for_students = forms.BooleanField(initial=True, label=_('Student survey'), required=False)
    for_mentors = forms.BooleanField(initial=False, label=_('Mentor survey'), required=False)

    class Meta:
        model = Survey

def sort_key(obj):
    return obj.index

def choice_list(field):    
    return [ (choice.pk, choice.name) for choice in Choice.objects.filter(field=field) ]
 
def clean_choice(value):
    if isinstance(value, list):
        return [ int(x) for x in value ]
    return [ int(value) ]

class SurveyForm(forms.Form):
    def __init__(self, survey, post=None):
        if post == None:
            forms.Form.__init__(self)
        else:
            forms.Form.__init__(self, post)

        fields = []
        for field in TextField.objects.filter(survey=survey):
            fields.append(field)
        for field in BooleanField.objects.filter(survey=survey):
            fields.append(field)
        for field in ChoiceField.objects.filter(survey=survey):
            fields.append(field)
        fields = sorted(fields, key=sort_key)

        for field in fields:
            if isinstance(field, TextField):
                self.fields['field-' + str(field.index)] = forms.CharField(label=field.name, required=field.required)
            elif isinstance(field, BooleanField):   
                self.fields['field-' + str(field.index)] = forms.BooleanField(label=field.name, required=False)
            else:
                form_field = None
                if field.multichoice:
                    form_field = forms.MultipleChoiceField(label=field.name, choices=choice_list(field), required=field.required, widget=forms.CheckboxSelectMultiple)
                else:
                    form_field = forms.ChoiceField(label=field.name, choices=choice_list(field), required=field.required, widget=forms.RadioSelect)
                self.fields['field-' + str(field.index)] = form_field

    def save(self, survey, user):
        if CompletedSurvey.objects.filter(survey=survey, user=user).count() != 0:
            raise Exception, 'User already completed survey'

        if not self.is_valid():
            raise Exception, 'Cannot save data from an invalid form'        

        fields = { }
        for field in TextField.objects.filter(survey=survey):
            fields[field.index] = field
        for field in BooleanField.objects.filter(survey=survey):
            fields[field.index] = field
        for field in ChoiceField.objects.filter(survey=survey):
            fields[field.index] = field

        CompletedSurvey(survey=survey, user=user).save()

        for (field, value) in self.cleaned_data.items():
            index = int(field[6:])
            currentField = fields[index]

            if isinstance(currentField, TextField) and value:
                (answer, created) = TextFieldAnswer.objects.get_or_create(field=currentField, user=user)
                answer.answer = value
                answer.save()
            elif isinstance(currentField, BooleanField) and value:
                (answer, created) = BooleanFieldAnswer.objects.get_or_create(field=currentField, user=user)
                answer.save()
            elif isinstance(currentField, ChoiceField):
                for choice in clean_choice(value):
                    (answer, created) = UserChoice.objects.get_or_create(choice=get_object_or_404(Choice, pk=choice), user=user)
                    answer.save()


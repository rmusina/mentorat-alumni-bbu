from django import forms
from profiles.models import *
from friends.models import Friendship, MentoringAgreement
from django.utils.translation import ugettext_lazy as _
from uni_form.helpers import FormHelper, Submit, Layout, Fieldset, HTML

error_messages_charfields = { 'required': _('This field is required'), 'max_length': _('You input is too long'),
                              'min_length': _('You input is too short') }

class MentoringAgreementForm(forms.Form):
    from_user = ''
    to_user = ''

    objective1 = forms.CharField(widget=forms.TextInput(),required=False, label=('1.'), error_messages=error_messages_charfields, max_length=80)
    objective2 = forms.CharField(required=False, label=_('2.'), error_messages=error_messages_charfields, max_length=40)
    objective3 = forms.CharField(required=False, label=_('3.'), error_messages=error_messages_charfields, max_length=40)

    communication1 = forms.CharField(required=False, label=_('1.'), error_messages=error_messages_charfields, max_length=40)
    communication2 = forms.CharField(required=False, label=_('2.'), error_messages=error_messages_charfields, max_length=40)
    communication3 = forms.CharField(required=False, label=_('3.'), error_messages=error_messages_charfields, max_length=40)

    activity1 = forms.CharField(required=False, label=_('1.'), error_messages=error_messages_charfields, max_length=40)
    activity2 = forms.CharField(required=False, label=_('2.'), error_messages=error_messages_charfields, max_length=40)
    activity3 = forms.CharField(required=False, label=_('3.'), error_messages=error_messages_charfields, max_length=40)

    objective_goals1 = forms.CharField(required=False, label=_('1.'), error_messages=error_messages_charfields, max_length=40)
    objective_goals2 = forms.CharField(required=False, label=_('2.'), error_messages=error_messages_charfields, max_length=40)
    objective_goals3 = forms.CharField(required=False, label=_('3.'), error_messages=error_messages_charfields, max_length=40)

    problem1 = forms.CharField(required=False, label=_('1.'), error_messages=error_messages_charfields, max_length=40)
    problem2 = forms.CharField(required=False, label=_('2.'), error_messages=error_messages_charfields, max_length=40)
    problem3 = forms.CharField(required=False, label=_('3.'), error_messages=error_messages_charfields, max_length=40)

    helper = FormHelper()
    layout = Layout(
        # options fieldset
        Fieldset(_("We set to achieve the following goals during this mentorship session:"), 'objective1', 'objective2', 'objective3'),
        Fieldset(_("Communication means and their frequency:"), 'communication1', 'communication2', 'communication3'),
        Fieldset(_("Proposed activities:"), 'activity1', 'activity2', 'activity3'),
        Fieldset(_("How will we know if our objectives are reached?"), 'objective_goals1', 'objective_goals2', 'objective_goals3'),
        Fieldset(_("Possible problems:"), 'problem1', 'problem2', 'problem3')
    )
    helper.add_layout(layout)
    submit = Submit('save', 'Save Information')
    helper.add_input(submit)
    def __init__(self, from_user, to_user, *args, **kwargs):
        super(MentoringAgreementForm, self).__init__(*args, **kwargs)
        self.from_user = from_user
        self.to_user = to_user

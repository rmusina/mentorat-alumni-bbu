from django import forms
from profiles.models import Event
from django.utils.translation import ugettext_lazy as _

class EventsForm(forms.ModelForm):

    class Meta:
        model = Event


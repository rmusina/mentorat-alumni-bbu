from django import forms
from profiles.models import Event
from django.utils.translation import ugettext_lazy as _

from django.utils.safestring import mark_safe

class EventsForm(forms.ModelForm):
    location = forms.CharField(label=mark_safe('Event Location (<a onclick="store_form_data_and_redirect()">chooose on map</a>)'))
    
    class Meta:
        model = Event




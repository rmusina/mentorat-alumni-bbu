from django import forms
from django.forms.forms import BoundField
from locations.widgets import LocationWidget, LocationFormField, LocationField, MapTypes
from locations.models import UserLocation

class UserLocationForm(forms.Form):
    
    #user = None
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        
        defaults = {}
        defaults['map_type'] = MapTypes.USER_LOCATION;
        defaults['location'] = kwargs.get('location', None)
        defaults['location'] = kwargs.get('pushpin', None)
        defaults.update(**kwargs)
        
        #print 'aaaaaaaaaaa1'  + defaults['location'].latitude 
        print len(args)
        
        user_location = LocationField().formfield(**{ 'widget' : LocationWidget(attrs=defaults)})
        
        super(UserLocationForm, self).__init__(*args, **kwargs)
    
    def save(self, request_data):
        if self.user == None:
            return
        
        latitude, longitude = LocationFormField().clean(request_data)

        #get address and stuff with reverse geoloc
        
        current_user_location = UserLocation.objects.filter(user=self.user)[0]
        
        if current_user_location == None:
            current_user_location = UserLocation()
            
        current_user_location.user = self.user
        current_user_location.latitude = latitude
        current_user_location.longitude = longitude
        
        current_user_location.save()
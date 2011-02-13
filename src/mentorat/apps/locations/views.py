import geopy.distance
import geopy.units
import datetime

from urllib2 import HTTPError
from geopy import geocoders

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from locations.models import UserLocation
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured

try:
    from notification import models as notification
except ImportError:
    notification = None

@login_required
def all_locations(request):
    
    return render_to_response("locations/locations.html",
        {'locations': UserLocation.objects },
        context_instance=RequestContext(request)
    )

@login_required
def your_location(request):
    
    user_location = UserLocation.objects.filter(user=request.user)
    
    if user_location == None:
        user_location = UserLocations()
        user_location.user = request.user
        if not user_location.set_from_account_data(request.user):
            user_location = None
        #if userLocation.setFromAccountData(request.user):
        #    userLocation.save() 
        
    return render_to_response("locations/your_location.html",
                              { 'user_location' : user_location },
                              context_instance=RequestContext(request)
                              )

import geopy.distance
import geopy.units
import datetime
import django.utils.simplejson

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from locations.models import UserLocation
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.exceptions import ImproperlyConfigured

from locations.forms import UserLocationForm

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

def get_pushpin_avatar(user):
    #user = User.objects.get(username=user)
    if user.is_staff:
        return '/site_media/media/pushpins/root.png'
    else:
        if user.get_profile().as_student() <> None:
            return '/site_media/media/pushpins/user.png'
        else:
            return '/site_media/media/pushpins/mentor.png'

@login_required
def user_location(request, form_class=UserLocationForm):
    
    if request.method == 'POST':
        form = form_class(request.user, request.POST, {'pushpin' : get_pushpin_avatar(request.user)})
        form.save(request.POST.get('user_location', '0,0'))        
    else:
        user_location = UserLocation.objects.filter(user=request.user).get(0)
        form = form_class(user_location, {'pushpin' : get_pushpin_avatar(request.user)})
        
    return render_to_response("locations/your_location.html",
                              { 'form' : form },
                              context_instance=RequestContext(request)
                              )

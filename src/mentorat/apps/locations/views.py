import json
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

from django.http import HttpResponseRedirect, HttpResponse
from locations.forms import UserLocationForm
from locations.models import UserLocation

try:
    from notification import models as notification
except ImportError:
    notification = None

@login_required
def all_locations(request):
    raise Http404
    return render_to_response("locations/locations.html",
        {'locations': UserLocation.objects },
        context_instance=RequestContext(request)
    )

def get_pushpin_avatar(user):
    #user = User.objects.get(username=user)
    raise Http404
    if user.is_staff:
        return '/site_media/media/pushpins/root.png'
    else:
        if user.get_profile().as_student() <> None:
            return '/site_media/media/pushpins/user.png'
        else:
            return '/site_media/media/pushpins/mentor.png'

@login_required
def user_location(request, form_class=UserLocationForm):
    raise Http404
    user_location = None
    
    if request.method == 'POST':
        print request.data       
    else:
        locations = UserLocation.objects.filter(user=request.user)
        user_location = None
        
        if len(locations) >= 1:
            user_location = locations[0]
                    
    return render_to_response("locations/your_location.html",
                              { 'user_location' : user_location,
                                'pushpin_path' : get_pushpin_avatar(request.user) },
                              context_instance=RequestContext(request)
                              )

@login_required
def map_data(request):
    raise Http404
    users = []
    for location in UserLocation.objects.all():
        user = location.user
        if user.is_staff or user.is_superuser:
            icon = 'root'
        elif user.get_profile().as_student():
            icon = 'student'
        else:
            icon = 'mentor'
        users.append({
            'name': user.username,
            'profile': reverse('profile_detail', kwargs={'username': user.username}),
            'lat': location.latitude,
            'lng': location.longitude,
            'icon': icon
        })

    data = {
        'users': users
    }
    return HttpResponse(status=200, mimetype="application/json", content=json.dumps(data))

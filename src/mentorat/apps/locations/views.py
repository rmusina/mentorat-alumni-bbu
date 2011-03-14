import geopy.distance
import geopy.units
import datetime
from django.utils import simplejson

from django.contrib.admin.views.decorators import staff_member_required
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
from locations.models import UserLocation, EventLocation
from friends.models import FriendshipInvitation
from geopy import geocoders

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
        return settings.STATIC_URL + 'pushpins/root.png'
    else:
        if user.get_profile().as_student() <> None:
            return settings.STATIC_URL + 'pushpins/user.png'
        else:
            return settings.STATIC_URL + 'pushpins/mentor.png'

@staff_member_required
def event_location(request):
    
    if request.method == "POST":
        json_data = simplejson.loads(request.raw_post_data)
        
        latitude = json_data["lat"]
        longitude = json_data["lng"]
        
        print latitude, longitude
        
        g = geocoders.Google()
        coord_string = "%s,%s" % (latitude, longitude)
        (place, point) = g.geocode(coord_string)
        
        request.session['events_selected_location'] = place
        request.session['events_selected_coordinates'] = coord_string
        
        return HttpResponse("/mentorship_admin/event_admin/")
    
    return render_to_response("locations/event_location.html",
                              context_instance=RequestContext(request))

@login_required
def user_location(request, form_class=UserLocationForm):
    user_location = None
    
    locations = UserLocation.objects.filter(user=request.user)
        
    if len(locations) >= 1:
        user_location = locations[0]
    
    if request.method == "POST":
        if user_location == None:
            user_location = UserLocation()
            user_location.user = request.user
        
        json_data = simplejson.loads(request.raw_post_data)
        user_location.latitude = json_data["lat"]
        user_location.longitude = json_data["lng"]
        
        user_location.save()
               
        return HttpResponse("Successfully saved new location.")       
                    
    return render_to_response("locations/your_location.html",
                              { 'user_location' : user_location,
                                'pushpin_path' : get_pushpin_avatar(request.user) },
                              context_instance=RequestContext(request)
                              )

@login_required
def all_locations(request):
    return render_to_response("locations/locations_all.html",
                              {},
                              context_instance=RequestContext(request)
                              )

@login_required
def map_data(request):
    users = []
    relations = []
    
    for location in UserLocation.objects.all():
        user = location.user
        if user.is_staff or user.is_superuser:
            icon = 'root'
        elif user.get_profile().as_student():
            icon = 'student'
        else:
            icon = 'mentor'
            for invitation in FriendshipInvitation.objects.filter(to_user=user):
                try: 
                     student = UserLocation.objects.get(user=invitation.from_user)
                     if student != None:
                         relations.append({'lat1':location.latitude, 'lng1':location.longitude,
                                      'lat2':student.latitude, 'lng2':student.longitude, 
                                      'status':invitation.status})
                except UserLocation.DoesNotExist:
                      pass                   
                    
        users.append({
            'profile' : '',#reverse('profile_detail', kwargs={'username': user.username}),
            'lat': location.latitude,
            'lng': location.longitude,
            'icon': icon
        })
    
    events = []
    for location in EventLocation.objects.all():
        event = location.event
        
        events.append({
            'event_details': reverse('event_details', kwargs={'eventId': event.id}),
            'lat': location.latitude,
            'lng': location.longitude
        })

    data = {
        'users': users,
        'events': events,
        'relations': relations
    }
    return HttpResponse(status=200, mimetype="application/json", content=simplejson.dumps(data))

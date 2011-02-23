from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language_from_request, ugettext_lazy as _
from geopy import geocoders  
from profiles.models import Profile
import urllib

def get_object_or_none(Class, **keys):
    objs = Class.objects.filter(**keys)
    if objs:
        return objs[0]
    return None

class UserLocation(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))    
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    #city = models.CharField(max_length=50)
    #country = models.CharField(max_length=50)
    #address = models.CharField(max_length=100)

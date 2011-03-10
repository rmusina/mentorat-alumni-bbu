from django.conf.urls.defaults import *

# Just a few url's. One for the new form and one for displaying checkins of the user and one for getting the search result
# and then checkin in to that place.

urlpatterns = patterns('',
    url(r'^$', 'locations.views.map_data', name='locations_all'),
    url(r'^your_location/$', 'locations.views.user_location', name='locations_your'),
    url(r'^event_location/$', 'locations.views.event_location', name='locations_event'),
    url(r'^data/$', 'locations.views.map_data', name='map_data'),
)

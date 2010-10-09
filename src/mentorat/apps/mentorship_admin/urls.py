from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^invite_users/$', 'mentorship_admin.views.admin_invite_users', name='admin_invite_users'),
    url(r'^search/$', 'mentorship_admin.views.admin_profiles', name='admin_profiles'),
    url(r'^event_admin/$', 'mentorship_admin.views.admin_events', name='admin_events'),
    url(r'^visibility/(?P<username>[\w\._-]+)/(?P<visibility>[\w\._-]+)/$', 'mentorship_admin.views.admin_set_profile_visibility', name='admin_set_visibility'),
)

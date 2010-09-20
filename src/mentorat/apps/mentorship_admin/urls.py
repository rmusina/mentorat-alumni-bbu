from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'invite_users/$', 'mentorship_admin.views.admin_invite_users', name='admin_invite_users'),
    url(r'search/$', 'mentorship_admin.views.admin_profiles', name='admin_profiles'),
)

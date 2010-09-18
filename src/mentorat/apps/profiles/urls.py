from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^username_autocomplete/$', 'autocomplete_app.views.username_autocomplete_friends', name='profile_username_autocomplete'),
    url(r'^$', 'profiles.views.profiles', name='profile_list'),
    url(r'^profile/(?P<username>[\w\._-]+)/$', 'profiles.views.profile', name='profile_detail'),
    url(r'^edit/general/$', 'profiles.views.profile_edit', {'section': 'general'}, name='profile_edit_general'),
    url(r'^edit/employment/$', 'profiles.views.profile_edit', {'section': 'employment', }, name='profile_edit_employment'),
    url(r'^edit/professional/$', 'profiles.views.profile_edit', {'section': 'professional', }, name='profile_edit_professional'),
    url(r'^edit/additional/$', 'profiles.views.profile_edit', {'section': 'additional', }, name='profile_edit_additional'),
)

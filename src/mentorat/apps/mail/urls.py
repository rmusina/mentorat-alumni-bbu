from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^confirm/(?P<key>[a-fA-F0-9]+)/$', 'mail.views.confirm', name='email_confirm'),
)

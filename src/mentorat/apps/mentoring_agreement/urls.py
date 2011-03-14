from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^agreements/$', 'mentoring_agreement.views.agreements', name='mentoring_agreements'),
    url(r'^agreement/(?P<username>[\w\._-]+)/$', 'mentoring_agreement.views.agreement', name='mentoring_agreement'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('surveys.views',
        url('^add/$', 'add_survey', name='add_survey'),
        url('^remove/(?P<id>\d+)/$', 'rm_survey', name='remove_survey'),
        )

from django.conf.urls.defaults import *

urlpatterns = patterns('',
        url('^add/$', 'surveys.views.add_survey', name='add_survey'),
        url('^add/success/$', 'django.views.generic.simple.direct_to_template', {'template': 'surveys/add_success.html'}, name='survey_add_success'),
        url('^take/(?P<id>\d+)/$', 'surveys.views.survey', name='survey_take'),
        url('^take/success/$', 'django.views.generic.simple.direct_to_template', {'template': 'surveys/take_success.html'}, name='survey_take_success'),
        )

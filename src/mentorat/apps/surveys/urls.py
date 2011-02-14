from django.conf.urls.defaults import *
from surveys.models import *

urlpatterns = patterns('',
        url('^add/$', 'surveys.views.add_survey', name='add_survey'),
        url('^add/success/$', 'django.views.generic.simple.direct_to_template', {'template': 'surveys/add_success.html'}, name='survey_add_success'),
        url('^take/(?P<id>\d+)/$', 'surveys.views.survey', name='survey_take'),
        url('^take/success/$', 'django.views.generic.simple.direct_to_template', {'template': 'surveys/take_success.html'}, name='survey_take_success'),
		url('^view/(?P<id>\d+)/(?P<username>[\w\._-]+)/$', 'surveys.views.view_user_input', name='survey_user_input'),
		url('^list/', 'surveys.views.survey_list', name='survey_list'),
        url('^stats/(?P<id>\d+)/$', 'surveys.views.stats', name='survey_stats'),
        url('^stats/(?P<id>\d+)/users/$', 'surveys.views.stats_userlist', name='survey_stats_users'),
        )

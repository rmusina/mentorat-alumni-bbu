from django.conf.urls.defaults import *

# for voting
from voting.views import vote_on_object
from bookmarks.models import Bookmark

urlpatterns = patterns('',
    url(r'^$', 'bookmarks.views.bookmarks', name="all_bookmarks"),
    url(r'^add/$', 'bookmarks.views.add', name="add_bookmark"),
    url(r'^/articles/(?P<newsId>\d+)/', 'bookmarks.views.news_details', name="news_details"),
    url(r'^/event_calendar/$', 'bookmarks.views.events_thisMonth', name="event_calendar_thisMonth"),
    url(r'^/event_calendar/(?P<pYear>\d{4})/(?P<pMonth>\d{1,2})/', 'bookmarks.views.events', name="event_calendar"),
    url(r'^/events/(?P<eventId>\d+)/', 'bookmarks.views.event_details', name="event_details"),
    url(r'^(\d+)/delete/$', 'bookmarks.views.delete', name="delete_bookmark_instance"),
)

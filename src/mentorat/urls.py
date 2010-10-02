from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from account.openid_consumer import PinaxConsumer
from blog.feeds import BlogFeedAll, BlogFeedUser
from bookmarks.feeds import BookmarkFeed
from microblogging.feeds import TweetFeedAll, TweetFeedUser, TweetFeedUserWithFriends

blogs_feed_dict = {"feed_dict": {
    'all': BlogFeedAll,
    'only': BlogFeedUser,
}}


if settings.ACCOUNT_OPEN_SIGNUP:
    signup_view = "account.views.signup"
else:
    signup_view = "signup_codes.views.signup"


urlpatterns = patterns('',
    url(r'^$', direct_to_template, {
        "template": "homepage.html",
    }, name="home"),


    url(r'^admin/invite_user/$', 'signup_codes.views.admin_invite_user', name="admin_invite_user"),
    url(r'^account/signup/$', signup_view, name="acct_signup"),

    (r'^mentorship_admin/', include('mentorship_admin.urls')),
    (r'^about/', include('about.urls')),
    (r'^account/', include('account.urls')),
    (r'^bbauth/', include('bbauth.urls')),
    (r'^authsub/', include('authsub.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^tags/', include('tag_app.urls')),
    (r'^invitations/', include('friends_app.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^announcements/', include('announcements.urls')),
    (r'^tribes/', include('tribes.urls')),
    (r'^comments/', include('threadedcomments.urls')),
    (r'^robots.txt$', include('robots.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^admin/(.*)', admin.site.root),
    (r'^avatar/', include('avatar.urls')),
    (r'^swaps/', include('swaps.urls')),
    (r'^flag/', include('flag.urls')),
    (r'^locations/', include('locations.urls')),
    (r'^wiki/', include('wiki.urls')),
    (r'^survey/', include('surveys.urls')),
    
    (r'^feeds/posts/(.*)/$', 'django.contrib.syndication.views.feed', blogs_feed_dict),
)


## @@@ for now, we'll use friends_app to glue this stuff together


from microblogging.models import Tweet

friends_tweets_kwargs = {
    "template_name": "microblogging/friends_tweets.html",
    "friends_objects_function": lambda users: Tweet.objects.filter(sender_id__in=[user.id for user in users], sender_type__name='user'),
}

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )

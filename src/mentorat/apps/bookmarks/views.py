from datetime import datetime, date
import urlparse
import urllib2

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from django.utils.translation import ugettext_lazy as _

from bookmarks.models import Bookmark, BookmarkInstance, EventCalendar
from bookmarks.forms import BookmarkInstanceForm
from django.utils.safestring import mark_safe

from profiles.models import Event
from calendar import monthrange

def bookmarks(request):
    bookmarks = Bookmark.objects.all().order_by("-added")
    if request.user.is_authenticated():
        user_bookmarks = Bookmark.objects.filter(saved_instances__user=request.user)
    else:
        user_bookmarks = []
    return render_to_response("bookmarks/bookmarks.html", {
        "bookmarks": bookmarks,
        "user_bookmarks": user_bookmarks,
    }, context_instance=RequestContext(request))


@login_required
def your_bookmarks(request):
    bookmark_instances = BookmarkInstance.objects.filter(user=request.user).order_by("-saved")
    return render_to_response("bookmarks/your_bookmarks.html", {
        "bookmark_instances": bookmark_instances,
    }, context_instance=RequestContext(request))

@login_required
def add(request):
    
    if request.method == "POST":
        bookmark_form = BookmarkInstanceForm(request.user, request.POST)
        if bookmark_form.is_valid():
            bookmark_instance = bookmark_form.save(commit=False)
            bookmark_instance.user = request.user
            bookmark_instance.save()
            bookmark = bookmark_instance.bookmark
            
            try:
                headers = {
                    "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                    "Accept-Language" : "en-us,en;q=0.5",
                    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Connection" : "close",
                    ##"User-Agent": settings.URL_VALIDATOR_USER_AGENT
                    }
                req = urllib2.Request(bookmark.get_favicon_url(force=True), None, headers)
                u = urllib2.urlopen(req)
                has_favicon = True
            except:
                has_favicon = False
            
            bookmark.has_favicon = has_favicon
            bookmark.favicon_checked = datetime.now() 
            bookmark.save()
            
            if bookmark.url == "":
                bookmark.url = reverse('news_details', kwargs={'newsId':bookmark.id}) 
                bookmark.save()
                
            if bookmark_form.should_redirect():
                return HttpResponseRedirect(bookmark.url)
            else:
                request.user.message_set.create(message=_("You have saved news '%(description)s'") % {'description': bookmark_instance.description})
                return HttpResponseRedirect(reverse("bookmarks.views.bookmarks"))
    else:
        initial = {}
        if "url" in request.GET:
            initial["url"] = request.GET["url"]   
        if "description" in request.GET:
            initial["description"] = request.GET["description"].strip()
        if "redirect" in request.GET:
            initial["redirect"] = request.GET["redirect"]
        
        if initial:
            bookmark_form = BookmarkInstanceForm(initial=initial)
        else:
            bookmark_form = BookmarkInstanceForm()
    
    bookmarks_add_url = "http://" + Site.objects.get_current().domain + reverse(add)
    bookmarklet = "javascript:location.href='%s?url='+encodeURIComponent(location.href)+';description='+encodeURIComponent(document.title)+';redirect=on'" % bookmarks_add_url
    
    return render_to_response("bookmarks/add.html", {
        "bookmarklet": bookmarklet,
        "bookmark_form": bookmark_form,
    }, context_instance=RequestContext(request))

@login_required
def delete(request, bookmark_instance_id):
    
    bookmark_instance = get_object_or_404(BookmarkInstance, id=bookmark_instance_id)
    if request.user == bookmark_instance.user:
        bookmark_instance.delete()
        request.user.message_set.create(message=_("News Post Deleted"))
        
    if "next" in request.GET:
        next = request.GET["next"]
    else:
        next = reverse("bookmarks.views.bookmarks")
    
    return HttpResponseRedirect(next)

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return date(1900, pMonthNumber, 1).strftime('%B')

def events_thisMonth(request):
    now = datetime.now()
    return events(request, now.year, now.month)

def news_details(request, newsId):
    
    news = Bookmark.objects.get(id=newsId)
    title = news.description
    description = news.note
    date = news.added.date()
    
    return render_to_response("bookmarks/news_details.html", 
                              {'title': title,
                               'date': date,
                               'description': description,}, 
                              context_instance=RequestContext(request));

def events(request, pYear, pMonth):
    pYear = int(pYear)
    pMonth = int(pMonth)
    if (pMonth > 12 or pMonth < 1):
        raise Http404
        
    my_events = Event.objects.order_by('date').filter(date__year=pYear, date__month=pMonth)
    
    cal = EventCalendar(my_events).formatmonth(pYear, pMonth)
    
    lPreviousYear = pYear
    lPreviousMonth = pMonth - 1
    
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = pYear - 1
    
    lNextYear = pYear
    lNextMonth = pMonth + 1
    
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = pYear + 1

    return render_to_response("bookmarks/event_calendar.html", 
                              {'calendar': mark_safe(cal),
                               'Month' : pMonth,
                               'MonthName' : named_month(pMonth),
                               'Year' : pYear,
                               'PreviousMonth' : lPreviousMonth,
                               'PreviousMonthName' : named_month(lPreviousMonth),
                               'PreviousYear' : lPreviousYear,
                               'NextMonth' : lNextMonth,
                               'NextMonthName' : named_month(lNextMonth),
                               'NextYear' : lNextYear,}, 
                              context_instance=RequestContext(request)); 
    
def event_details(request, eventId):

    event = Event.objects.get(id=eventId)
    return render_to_response("bookmarks/event_details.html",
                              {'name': event.name,
                               'location': event.location,
                               'date': event.date,
                               'description': event.description,
                               'points': event.points},
                              context_instance=RequestContext(request));
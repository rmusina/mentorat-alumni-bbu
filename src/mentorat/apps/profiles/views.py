from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from friends.forms import InviteFriendForm
from friends.models import FriendshipInvitation, Friendship

from microblogging.models import Following

from profiles.models import *
from profiles.forms import *
from profiles.forms_parts import *

from messages.forms import ComposeForm

from avatar.templatetags.avatar_tags import avatar
from django.contrib.admin.views.decorators import staff_member_required
import datetime

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

import hashlib, zlib
import cPickle as pickle

@login_required
def profiles(request, template_name="profiles/profiles.html", extra_context=None):
    if extra_context is None:
        extra_context = {}

    users = None

    if request.user.is_staff:
        users = Profile.objects.all()
    else:
        profile = request.user.get_profile()
        if profile.as_student() != None:
            users = MentorProfile.objects.all()
        else:
            if profile.as_mentor().visible_to_mentors:
                users = MentorProfile.objects.filter(visible_to_mentors=True)
            else:
                return render_to_response('profiles/not_visible_mentor.html', {}, context_instance=RequestContext(request))

    if request.user.is_staff:
        users = users.filter(user__is_staff=False)
    else:
        users = users.filter(user__is_staff=False, user__is_active=True)

    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(user__username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-user__date_joined")
    elif order == 'name':
        users = users.order_by("user__username")
    elif order == 'faculty':
        users = users.order_by("")
    return render_to_response(template_name, dict({
        'users': users,
        'order': order,
        'search_terms': search_terms,
    }, **extra_context), context_instance=RequestContext(request))


def get_object_or_none(Class, **keys):
    objs = Class.objects.filter(**keys)
    if objs:
        return objs[0]
    return None
    

@login_required
def profile(request, username, template_name="profiles/profile.html", extra_context=None):    
    if extra_context is None:
        extra_context = {}
    
    other_user = get_object_or_none(User, username=username)
    if other_user == None or other_user.is_staff or (not other_user.get_profile().active and request.user != other_user and not request.user.is_staff) or (not other_user.is_active and not request.user.is_staff):
        return render_to_response('profiles/profile_404.html', context_instance=RequestContext(request))
    
    if request.user.is_authenticated():
        is_friend = Friendship.objects.are_friends(request.user, other_user)
        is_following = Following.objects.is_following(request.user, other_user)
        other_friends = Friendship.objects.friends_for_user(other_user)
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        other_friends = []
        is_friend = False
        is_me = False
        is_following = False
    
    if is_friend:
        invite_form = None
        previous_invitations_to = None
        previous_invitations_from = None
        if request.method == "POST":
            if request.POST.get("action") == "remove": # @@@ perhaps the form should just post to friends and be redirected here
                Friendship.objects.remove(request.user, other_user)
                request.user.message_set.create(message=_("You have removed %(from_user)s from mentor contacts") % {'from_user': other_user})
                is_friend = False
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                    'message': ugettext("Please review my cv and accept my request!"),
                })
    else:
        if request.user.is_authenticated() and request.method == "POST":
            if request.POST.get("action") == "invite": # @@@ perhaps the form should just post to friends and be redirected here
                invite_form = InviteFriendForm(request.user, request.POST)
                if invite_form.is_valid():
                    invite_form.save()
            elif request.POST.get("action")  == "renounce":
                invitation = FriendshipInvitation.objects.sent_invitations(to_user=other_user, from_user=request.user)[0]
                invitation.renounce()
                request.user.message_set.create(message=_("You have chosen to renounce this request %(from_user)s") % {'from_user': invitation.from_user})
                invite_form = None
            else:
                invite_form = InviteFriendForm(request.user, {
                    'to_user': username,
                    'message': ugettext("Please review my cv and accept my request!"),
                })
                invitation_id = request.POST.get("invitation", None)
                if request.POST.get("action") == "accept": # @@@ perhaps the form should just post to friends and be redirected here
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.accept()
                            request.user.message_set.create(message=_("You have accepted the mentorship request from %(from_user)s") % {'from_user': invitation.from_user})
                            is_friend = True
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass
                elif request.POST.get("action") == "decline": # @@@ perhaps the form should just post to friends and be redirected here
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.decline()
                            request.user.message_set.create(message=_("You have declined the mentorship request from %(from_user)s. Please write a message to this user motivating your decision.") % {'from_user': invitation.from_user})
                            other_friends = Friendship.objects.friends_for_user(other_user)
                                   
                        return HttpResponseRedirect(reverse('messages.views.compose', kwargs={'recipient':invitation.from_user}))
                    except FriendshipInvitation.DoesNotExist:
                        pass
                elif request.POST.get("action") == "pending": # @@@ perhaps the form should just post to friends and be redirected here
                    try:
                        invitation = FriendshipInvitation.objects.get(id=invitation_id)
                        if invitation.to_user == request.user:
                            invitation.pending()
                            request.user.message_set.create(message=_("You have chosen to review the mentorship request from %(from_user)s") % {'from_user': invitation.from_user})
                            other_friends = Friendship.objects.friends_for_user(other_user)
                    except FriendshipInvitation.DoesNotExist:
                        pass                
        else:
            invite_form = InviteFriendForm(request.user, {
                'to_user': username,
                'message': ugettext("Please review my cv and accept my request!"),
            })
    
    previous_invitations_to = FriendshipInvitation.objects.invitations(to_user=other_user, from_user=request.user)
    previous_invitations_from = FriendshipInvitation.objects.invitations(to_user=request.user, from_user=other_user)
    previous_denied_invitation_to =  FriendshipInvitation.objects.invitationsDenied(to_user=other_user, from_user=request.user)
    
    deny_mentor_request = False
    consumed_all_requests = False
    mentor_can_accept = False
    
    if request.user.is_authenticated and not request.user.is_staff:
        if request.user.get_profile().as_student() == None or other_user.get_profile().as_mentor() == None:
            deny_mentor_request = True
        
        consumed_all_requests = FriendshipInvitation.objects.countRequests(from_user = request.user) >= 3
    
        if request.user.get_profile().as_mentor() != None and FriendshipInvitation.objects.countAccepts(to_user = request.user) < 3:
            mentor_can_accept = True

    mentor = None
    if not request.user.is_staff and not request.user.is_superuser:
        mentor = request.user.get_profile().as_mentor()
    other_mentor = other_user.get_profile().as_mentor()
    if mentor != None and other_mentor != None and mentor != other_mentor:
        if not mentor.visible_to_mentors or not other_mentor.visible_to_mentors:
            raise Http404
    
    users_know_each_other = Friendship.objects.are_friends(request.user, other_user)
    print 'Friends:', users_know_each_other

    allow_private = is_me or request.user.is_staff
    allow_restricted = is_me or request.user.is_staff or users_know_each_other
    
    return render_to_response(template_name, dict({
        "invitations_active_on_platform": settings.ALLOW_MENTORING_REQUESTS,
        "is_me": is_me,
        "is_friend": is_friend,
        "is_following": is_following,
        "other_user": other_user,
        "allow_private": allow_private, # can see private fields
        "allow_restricted": allow_restricted, # can see restricted fields
        "has_mentor": FriendshipInvitation.objects.hasMentor(from_user = request.user),
        "deny_mentor_request": deny_mentor_request, #can see the 'add as a friend' field
        "consumed_all_requests": consumed_all_requests,
        "student": other_user.get_profile().as_student(),
        "mentor": other_user.get_profile().as_mentor(),
        "mentor_can_accept": mentor_can_accept,
        "other_friends": other_friends,
        "invite_form": invite_form,
        "previous_invitations_to": previous_invitations_to,
        "previous_invitations_from": previous_invitations_from,
        "previous_denied_invitation_to": previous_denied_invitation_to,
    }, **extra_context), context_instance=RequestContext(request))


@login_required
def profile_edit(request, form_class=GeneralInfoForm, **kwargs):
    template_name = kwargs.get("template_name", "profiles/profile_edit.html")
    section = kwargs.get('section')
    
    if request.is_ajax():
        template_name = kwargs.get(
            "template_name_facebox",
            "profiles/profile_edit_facebox.html"
        )
    
    profile = request.user.get_profile()
    student=False
    mentor=False
    if profile.as_student():
        profile = profile.as_student()
        student=True
    elif profile.as_mentor():
        profile = profile.as_mentor()
        mentor=True
    else:
        raise Http404

    # select for type
    section_verbose_name = ''
    post_url = ''
    if section == 'general':
        if student:
            form_class = StudentGeneralInfoForm
        else:
            form_class = MentorGeneralInfoForm
        section_verbose_name = _('General information')
        post_url = reverse('profile_edit_general')
    elif section == 'employment':
        if student:
            form_class = StudentEmploymentForm
        else:
            form_class = MentorEmploymentForm
        section_verbose_name = _('Current employment')
        post_url = reverse('profile_edit_employment')
    elif section == 'professional':
        if student:
            form_class = StudentProfessionalForm
        else:
            form_class = MentorProfessionalForm
        section_verbose_name = _('Academic and professional information')
        post_url = reverse('profile_edit_employment')
    elif section == 'additional':
        if student:
            form_class = StudentAdditionalForm
        else:
            form_class = MentorAdditionalForm
        section_verbose_name = _('Additional information')
        post_url = reverse('profile_edit_additional')
    else:
        raise Http404

    
    if request.method == "POST":
        profile_form = form_class(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse("profile_detail", args=[request.user.username]))
    else:
        profile_form = form_class(instance=profile)
    
    return render_to_response(template_name, {
        "profile": profile,
        "profile_form": profile_form,
        "section": section,
        'section_verbose_name': section_verbose_name

    }, context_instance=RequestContext(request))

@login_required
def volunteer_remove(request, id):
    profile=request.user.get_profile()
    org = VolunteerOrganization.objects.filter(pk=id)
    if len(org):
        org = org[0]
        if org.profile == profile:
            org.delete()
    return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))

@login_required
def volunteer_add_or_edit(request, **kargs):
    add = kargs['type'] == 'add'
    if not add and kargs['type'] != 'edit':
        raise Http404
    
    page_title = _('Volunteer organization')
    post_url = ''
    submit_name = ''
    page_name = ''
    profile_url = reverse('profile_detail', args=[request.user.username])
    form = None
    if add:
        if request.method == 'POST':
            form = VolunteerForm(request.POST, instance=VolunteerOrganization())
            if form.is_valid():
                volunteer = form.save(commit=False)
                volunteer.profile = request.user.get_profile()
                volunteer.save()
                return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        else:
            form = VolunteerForm()
        post_url = reverse('volunteer_add')
        submit_name = _('Add')
        page_name = _('Add a volunteer organization in which you were a member')
    else: # edit
        id = kargs['id']
        orgs = VolunteerOrganization.objects.filter(pk=id)
        org = None
        good = True
        if len(orgs) == 0:
            good = False
        else:
            org = orgs[0]
        if good and org.profile != request.user.get_profile():
            good = False
        if not good:
            return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        
        if request.method == 'POST':
            form = VolunteerForm(request.POST, instance=org)
            if form.is_valid():
                org = form.save(commit=False)
                org.profile = request.user.get_profile()
                org.save()
                return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        else:
            form = VolunteerForm(instance=org)            
        
        post_url = reverse('volunteer_edit', args=[id])
        submit_name = _('Save')
        page_name = _('Update information about a volunteer organization')
    
    return render_to_response('profiles/profile-types/parts/form.html', 
                              {'form': form, 'post_url': post_url, 'submit_name': submit_name, 
                               'profile_url': profile_url, 'page_name': page_name, 'page_title': page_title},
                              context_instance=RequestContext(request))
    
@login_required
def employment_remove(request, id):
    student=request.user.get_profile().as_student()
    if student:
        job = StudentEmployment.objects.filter(pk=id)
        if len(job):
            job = job[0]
            if job.student == student:
                job.delete()
    return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
    
    
@login_required
def employment_add_or_edit(request, **kargs):
    student = request.user.get_profile().as_student()
    if not student:
        return HttpResponseRedirect(reverse('profile_detail'), args=[request.user.username])
    add = kargs['type'] == 'add'
    if not add and kargs['type'] != 'edit':
        raise Http404
    
    page_title = _('Work experience')
    post_url = ''
    submit_name = ''
    page_name = ''
    profile_url = reverse('profile_detail', args=[request.user.username])
    form = None
    if add:
        if request.method == 'POST':
            form = EmploymentForm(request.POST, instance=StudentEmployment())
            if form.is_valid():
                employment = form.save(commit=False)
                employment.student = student
                employment.save()
                return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        else:
            form = EmploymentForm()
        post_url = reverse('employment_add')
        submit_name = _('Add')
        page_name = _('Add information about your work experience')
    else: # edit
        id = kargs['id']
        employments = StudentEmployment.objects.filter(pk=id)
        now = None
        good = True
        if len(employments) == 0:
            good = False
        else:
            now = employments[0]
        if good and now.student != student:
            good = False
        if not good:
            return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        
        if request.method == 'POST':
            form = EmploymentForm(request.POST, instance=now)
            if form.is_valid():
                now = form.save(commit=False)
                now.student = student
                now.save()
                return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        else:
            form = EmploymentForm(instance=now)            
        
        post_url = reverse('employment_edit', args=[id])
        submit_name = _('Save')
        page_name = _('Update the information about you work experience')
    
    return render_to_response('profiles/profile-types/parts/form.html', 
                              {'form': form, 'post_url': post_url, 'submit_name': submit_name, 
                               'profile_url': profile_url, 'page_name': page_name, 'page_title': page_title},
                              context_instance=RequestContext(request))
    
@login_required
def research_remove(request, id):
    student=request.user.get_profile().as_student()
    if student:
        research = StudentResearch.objects.filter(pk=id)
        if len(research):
            research = research[0]
            if research.student == student:
                research.delete()
    return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
    
    
@login_required
def research_add_or_edit(request, **kargs):
    student = request.user.get_profile().as_student()
    if not student:
        return HttpResponseRedirect(reverse('profile_detail'), args=[request.user.username])
    add = kargs['type'] == 'add'
    if not add and kargs['type'] != 'edit':
        raise Http404
    
    page_title = _('Research')
    post_url = ''
    submit_name = ''
    page_name = ''
    profile_url = reverse('profile_detail', args=[request.user.username])
    form = None
    if add:
        if request.method == 'POST':
            form = ResearchForm(request.POST, instance=StudentResearch())
            if form.is_valid():
                research = form.save(commit=False)
                research.student = student
                research.save()
                return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        else:
            form = ResearchForm()
        post_url = reverse('research_add')
        submit_name = _('Add')
        page_name = _('Add information about your research activities')
    else: # edit
        id = kargs['id']
        researches = StudentResearch.objects.filter(pk=id)
        now = None
        good = True
        if len(researches) == 0:
            good = False
        else:
            now = researches[0]
        if good and now.student != student:
            good = False
        if not good:
            return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        
        if request.method == 'POST':
            form = ResearchForm(request.POST, instance=now)
            if form.is_valid():
                now = form.save(commit=False)
                now.student = student
                now.save()
                return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))
        else:
            form = ResearchForm(instance=now)            
        
        post_url = reverse('research_edit', args=[id])
        submit_name = _('Save')
        page_name = _('Update the information about your research activities')
    
    return render_to_response('profiles/profile-types/parts/form.html', 
                              {'form': form, 'post_url': post_url, 'submit_name': submit_name, 
                               'profile_url': profile_url, 'page_name': page_name, 'page_title': page_title},
                              context_instance=RequestContext(request))

COUNT_ON_PAGE = 50;

@login_required
def events(request, username):
    user = User.objects.filter(username=username)
    if not user:
        raise Http404
    user = user[0]
    student = StudentProfile.objects.get(user=user)
    events = StudentEvent.objects.filter(student=student)
    max = events.count()
    
    if 'offset' in request.GET:
        try:
            offset = int(request.GET['offset'])
        except:
            offset = 0
    else:
        offset = 0
    
    if offset < 0:
        offset = 0
        return HttpResponseRedirect(reverse('profile_events', args=[username]))
    
    if offset >= max and max:
        newoffset = int(max / COUNT_ON_PAGE) * COUNT_ON_PAGE
        if newoffset == max:
            newoffset -= COUNT_ON_PAGE
        else:
            newoffset -= 1
        return HttpResponseRedirect(reverse('profile_events', args=[username])+'?offset='+str(newoffset))
    
    prev = False
    next = False
    prev_offset = 0
    next_offset = 0
    last_offset = int(max / COUNT_ON_PAGE) * COUNT_ON_PAGE
    if last_offset == max: last_offset -= COUNT_ON_PAGE
    else: last_offset -= 1
     
    if offset:
        prev = True
        prev_offset = offset - COUNT_ON_PAGE
        if prev_offset < 0:
            prev_offset = 0
            
    if offset + COUNT_ON_PAGE < max:
        next = True
        next_offset = offset + COUNT_ON_PAGE

    return render_to_response('profiles/profile_events.html',
                              {'username': username, 'events': events[offset:offset+COUNT_ON_PAGE], 'prev_offset': prev_offset,
                               'next_offset': next_offset, 'last_offset': last_offset, 'prev': prev, 'next': next},
                               context_instance=RequestContext(request))


class AdminEvent:
    id = 0
    name = ''
    date = ''
    points = 0
    participated = False
    
    def __init__(self, id, name, date, points, participated):
        self.id = id
        self.name = name
        self.date = date
        self.points = points
        self.participated = participated


@staff_member_required
def admin_events(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_staff or not user.get_profile().as_student():
        raise Http404
    student = user.get_profile().as_student()    
    items = Event.objects.order_by('-date')
    
    # find number of objects and current offset
    count = items.count()
    offset = 0
    if 'offset' in request.GET:
        try:
            offset = int(request.GET['offset'])
        except:
            offset = 0
            
    # check validity of offset and redirect on invalid
    if offset and offset >= count:
        offset = max(0, count - COUNT_ON_PAGE)
        return HttpResponseRedirect(reverse('profile_admin_edit', args=[username])+'?offset='+str(offset))
    if offset < 0:
        return HttpResponseRedirect(reverse('profile_admin_edit', args=[username]))
    
    # compute next, previous, first and last offsets
    has_next = has_prev = False
    next = prev = 0
    last = max(0, count - COUNT_ON_PAGE)
    if offset > 0:
        prev = max(0, offset - COUNT_ON_PAGE)
        has_prev = True  
    if offset + COUNT_ON_PAGE < count:
        next = offset + COUNT_ON_PAGE
        has_next = True
        
    # on post save data
    save_message = None
    if request.method == "POST":
        ids = []
        checked = []
        for name in request.POST.keys():
            if name.startswith('event-'):
                try:
                    id = int(request.POST[name])
                    checked.append(id)
                except:
                    continue
            else:
                if name.startswith('id-event-'):
                    try:
                        id = int(request.POST[name])
                        ids.append(id)
                    except:
                        continue
                    
        for id in checked:
            event = get_object_or_none(Event, pk=id)
            if event != None:
                stud_event = get_object_or_none(StudentEvent, student=student, event=event)
                if stud_event == None:
                    stud_event = StudentEvent(student=student, event=event, date=datetime.datetime.now())
                    stud_event.save()
            ids.remove(id)
            
        for id in ids:
            obj = get_object_or_none(StudentEvent, student=student, event=get_object_or_none(Event, pk=id))
            if obj != None:
                obj.delete()
                      
        save_message = _('Changes were successfully saved')
        
    if 'redirect' in request.GET:
        return HttpResponseRedirect(request.GET['redirect'])
    
    # build the list of items to return
    items = items[offset: offset + COUNT_ON_PAGE]
    page_items = []
    for item in items:
        page_items.append(AdminEvent(item.pk, item.name, item.date, item.points, StudentEvent.objects.filter(student=student, event=item).count() > 0))
        
    return render_to_response('profiles/admin/events.html',
                              {'has_next': has_next, 'has_prev': has_prev, 
                               'next': next, 'last': last,
                               'prev': prev,
                               'offset': offset,
                               'username': username,
                               'save_message': save_message, 
                               'items': page_items}, context_instance = RequestContext(request))

        
@login_required  
def activate(request, state):
    print state
    if state == 'on':
        request.user.get_profile().active = True
    else:
        request.user.get_profile().active = False
    request.user.get_profile().save()
        
    return HttpResponseRedirect(reverse('profile_detail', args=[request.user.username]))

@login_required
def view_message(request, invitation_id):
       
    invitation = FriendshipInvitation.objects.get(id=invitation_id)
   
    if request.user == invitation.from_user or request.user == invitation.to_user:
        return render_to_response('profiles/view_message.html',
                              {'invitation':invitation}, 
                              context_instance = RequestContext(request))
    else:
        raise Http404
    
@login_required  
def apply(request, username):
    
    return  profile(request, username, "profiles/apply.html") #TODO: hack - consider adapting at first iteration


@login_required
def hide_from_mentors(request, username, visibility):
    if request.user.username != username or request.user.get_profile().as_mentor() == None or (visibility != 'on' and visibility != 'off'):
        raise Http404

    mentor = request.user.get_profile().as_mentor()
    mentor.visible_to_mentors = visibility == 'on'
    mentor.save()

    return HttpResponseRedirect(reverse('profile_detail', kwargs={ 'username': username }))

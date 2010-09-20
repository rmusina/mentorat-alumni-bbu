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

from avatar.templatetags.avatar_tags import avatar

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def profiles(request, template_name="profiles/profiles.html", extra_context=None):
    if extra_context is None:
        extra_context = {}
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, dict({
        'users': users,
        'order': order,
        'search_terms': search_terms,
    }, **extra_context), context_instance=RequestContext(request))


def profile(request, username, template_name="profiles/profile.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    other_user = get_object_or_404(User, username=username)
    
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
                            request.user.message_set.create(message=_("You have declined the mentorship request from %(from_user)s") % {'from_user': invitation.from_user})
                            other_friends = Friendship.objects.friends_for_user(other_user)
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
    previous_denied_invitation_to =  FriendshipInvitation.objects.invitationsDenied(to_user=request.user, from_user=other_user)
    
    if request.user.get_profile().as_student() == None or other_user.get_profile().as_mentor() == None:
        deny_mentor_request = True
    else: 
        deny_mentor_request = False
    
    return render_to_response(template_name, dict({
        "is_me": is_me,
        "is_friend": is_friend,
        "is_following": is_following,
        "other_user": other_user,
        "allow_private": is_me, # can see private fields
        "allow_restricted": True, # can see restricted fields
        "deny_mentor_request": deny_mentor_request, #can see the 'add as a friend' field
        "student": other_user.get_profile().as_student(),
        "mentor": other_user.get_profile().as_mentor(),
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
    
    
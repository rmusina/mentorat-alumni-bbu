from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.utils.translation import ugettext_lazy as _

from friends.models import *
from friends.forms import JoinRequestForm, FriendshipInvitation
from friends_app.forms import ImportVCardForm
from account.forms import SignupForm
from friends.importer import import_yahoo, import_google

# @@@ if made more generic these could be moved to django-friends proper

def friends(request, form_class=JoinRequestForm,
        template_name="friends_app/invitations.html"):
    if request.method == "POST":
        invitation_id = request.POST.get("invitation", None)
        if request.POST["action"] == "accept":
            try:
                invitation = FriendshipInvitation.objects.get(id=invitation_id)
                if invitation.to_user == request.user:
                    invitation.accept()
                    request.user.message_set.create(message=_("Accepted mentorship request from %(from_user)s") % {'from_user': invitation.from_user})
            except FriendshipInvitation.DoesNotExist:
                pass
            join_request_form = form_class()
        elif request.POST["action"] == "invite": # invite to join
            join_request_form = form_class(request.POST)
            
            if join_request_form.is_valid():
                join_request_form.save(request.user)
                join_request_form = form_class() # @@@
            
        elif request.POST["action"] == "decline":
            try:
                invitation = FriendshipInvitation.objects.get(id=invitation_id)
                if invitation.to_user == request.user:
                    invitation.decline()
                    request.user.message_set.create(message=_("Declined mentoring request from %(from_user)s. Please write a message to this user motivating your decision.") % {'from_user': invitation.from_user})
                return HttpResponseRedirect(reverse('messages.views.compose', kwargs={'recipient':invitation.from_user}))
            except FriendshipInvitation.DoesNotExist:
                pass
            join_request_form = form_class()
        elif request.POST["action"] == "pending":
            try:
                invitation = FriendshipInvitation.objects.get(id=invitation_id)
                if invitation.to_user == request.user:
                    invitation.pending()
                    request.user.message_set.create(message=_("You have chosen to overview this request %(from_user)s") % {'from_user': invitation.from_user})
            except FriendshipInvitation.DoesNotExist:
                pass
            join_request_form = form_class()
            
    else:
        join_request_form = form_class()
    
    invites_received = request.user.invitations_to.invitationsAll().order_by("-sent")
    invites_sent = request.user.invitations_from.invitationsAll().order_by("-sent")
    joins_sent = request.user.join_from.all().order_by("-sent")
    
    is_superuser = True
    
    if not request.user.is_superuser: 
        is_superuser = False
    
    is_mentor = False
    mentor_can_accept = False
    
    if not is_superuser:
        if request.user.get_profile().as_mentor() != None:
            is_mentor = True
        
        if request.user.get_profile().as_mentor() != None and FriendshipInvitation.objects.countAccepts(to_user = request.user) < 3:
            mentor_can_accept = True       
        
    return render_to_response(template_name, {
        "invitations_active_on_platform": settings.ALLOW_MENTORING_REQUESTS,
        "is_superuser" : is_superuser,
        "is_mentor" : is_mentor,
        "join_request_form": join_request_form,
        "mentor_can_accept": mentor_can_accept,
        "invites_received": invites_received,
        "invites_sent": invites_sent,
        "joins_sent": joins_sent,
    }, context_instance=RequestContext(request))
friends = login_required(friends)

def accept_join(request, confirmation_key, form_class=SignupForm,
        template_name="account/signup.html"):
    join_invitation = get_object_or_404(JoinInvitation, confirmation_key = confirmation_key.lower())
    if request.user.is_authenticated():
        return render_to_response("account/signup.html", {
        }, context_instance=RequestContext(request))
    else:
        form = form_class(initial={"email": join_invitation.contact.email, "confirmation_key": join_invitation.confirmation_key })
        return render_to_response(template_name, {
            "form": form,
        }, context_instance=RequestContext(request))

def friends_objects(request, template_name, friends_objects_function, extra_context={}):
    """
    Display friends' objects.
    
    This view takes a template name and a function. The function should
    take an iterator over users and return an iterator over objects
    belonging to those users. This iterator over objects is then passed
    to the template of the given name as ``object_list``.
    
    The template is also passed variable defined in ``extra_context``
    which should be a dictionary of variable names to functions taking a
    request object and returning the value for that variable.
    """
    
    friends = friend_set_for(request.user)
    
    dictionary = {
        "object_list": friends_objects_function(friends),
    }
    for name, func in extra_context.items():
        dictionary[name] = func(request)
    
    return render_to_response(template_name, dictionary, context_instance=RequestContext(request))
friends_objects = login_required(friends_objects)

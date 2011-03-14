from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext
from django.template.loader import render_to_string

from account.utils import get_default_redirect
from signup_codes.models import check_signup_code
from signup_codes.forms import SignupForm, InviteUserForm

from profiles.models import StudentProfile, MentorProfile, FieldOfInterest
from forms import EventsForm
from django.utils.translation import ugettext_lazy as _

import datetime
import profiles
import mail.utils

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


@staff_member_required
def admin_set_profile_visibility(request, username, visibility, template_name="mentorship_admin/admin_set_profile_visibility.html", extra_context=None):
    if extra_context == None:
        extra_context = {}

    other_user = get_object_or_404(User,username=username)
    if visibility == 'activate':
        if other_user.is_active == False:
            other_user.is_active = True
    elif visibility == 'deactivate':
        if other_user.is_active == True:
            other_user.is_active = False
    elif visibility == 'status':
        pass
    else:
        raise Http404

    email = profiles.models.Profile.objects.get(user=other_user).email
    
    if other_user.is_active:
        subject = 'Contul tau a fost activat'
    else:
        subject  = 'Contul tau a fost dezactivat'
    message = render_to_string('mentorship_admin/activate_message.txt', { 'active': other_user.is_active, 'username': username })
    mail.utils.mail(email, subject, message)

    if other_user.is_active == True:
        other_user_status = 'active'
        mail.utils.send_mail_confirm(other_user)
    else:
        other_user_status = 'inactive'
     

    other_user.save()

    return render_to_response(template_name, dict({
        'user': other_user,
        'status': other_user_status,
    }, **extra_context), context_instance=RequestContext(request))


@staff_member_required
def admin_profiles(request, template_name="mentorship_admin/admin_search_profiles.html", extra_context=None):
    if extra_context == None:
        extra_context = {}

    users = User.objects.all().order_by("-date_joined").exclude(is_superuser=True).exclude(is_active=False)
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    selected_field_index = request.GET.get('field')
    if (selected_field_index == "None"):
        selected_field_index = None

    nr_fields = FieldOfInterest.objects.count()
    selected_field_of_interest = None
    if selected_field_index:
        if 1 <= int(selected_field_index) <= nr_fields:
            selected_field_of_interest = FieldOfInterest.objects.get(pk=selected_field_index).name

    if not order:
        order = 'name'
    if search_terms:
        if order == 'name':
            users = users.filter(
                Q(username__icontains=search_terms) |
                Q(profile__firstname__icontains=search_terms) |
                Q(profile__surname__icontains=search_terms)
            )
        elif order == 'faculty':
            users = users.filter(
                Q(profile__studentprofile__faculty__icontains=search_terms)
            )

    if selected_field_of_interest:
        users = users.filter(profile__fields_of_interest__field__name__iexact=selected_field_of_interest)
    # order by date
    if order == 'date':
        users = users.order_by("-date_joined")
    # order by username
    elif order == 'name':
        users = users.order_by("username")
    elif order == 'faculty':
        users = users.order_by('profile__studentprofile__faculty')
    elif order == 'students':
        student_list = [stud.pk for stud in StudentProfile.objects.all()]
        users = users.filter(profile__pk__in=student_list)
    elif order == 'mentors':
        mentor_list = [m.pk for m in MentorProfile.objects.all()]
        users = users.filter(profile__pk__in=mentor_list)

    fields_of_interest = FieldOfInterest.objects.all()

    return render_to_response(template_name, dict({
        'users': users,
        'order': order,
        'search_terms': search_terms,
        'fields_of_interest': fields_of_interest,
        'field': selected_field_index,
    }, **extra_context), context_instance=RequestContext(request))


@staff_member_required
def admin_invite_users(request, form_class = InviteUserForm,
        template_name="mentorship_admin/admin_invite_users.html"):
    """
    View that works inside the admin tab
    """
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            form.send_signup_code()
            request.user.message_set.create(message=ugettext("An e-mail has been sent to %(email)s.") % {"email": email})
            form = form_class() # reset
    else:
        form = form_class()
    return render_to_response(template_name, {
        "title": ugettext("Invite user"),
        "form": form,
    }, context_instance = RequestContext(request))

def get_initial_form_values_from_session(request):
    ret_dict = {}
    
    ret_dict['name'] = request.session.get('events_selected_name', '')
    ret_dict['points'] = request.session.get('events_selected_points', '1')
    ret_dict['date'] = request.session.get('events_selected_date', datetime.datetime.now())
    ret_dict['location'] = request.session.get('events_selected_location', '')
    ret_dict['description'] = request.session.get('events_selected_description', '')
    
    return ret_dict

def set_form_session_values(request, data_dict):
    request.session['events_selected_name'] = data_dict.get('name', '')
    request.session['events_selected_points'] = data_dict.get('points', '')
    request.session['events_selected_date'] = data_dict.get('date', '')
    request.session['events_selected_location'] = data_dict.get('location', '')
    request.session['events_selected_description'] = data_dict.get('description', '')

def safely_delete_key(dict, key):
    if dict.has_key(key):
        del dict[key]

def cleanup_session_data(request):
    safely_delete_key(request.session, 'events_selected_name')
    safely_delete_key(request.session, 'events_selected_points')
    safely_delete_key(request.session, 'events_selected_date')
    safely_delete_key(request.session, 'events_selected_location')
    safely_delete_key(request.session, 'events_selected_description')
    

from locations.models import EventLocation

@staff_member_required
def admin_events(request, form_class = EventsForm,
        template_name="mentorship_admin/admin_events.html"):
    """
    View that controls the admin add events forms
    """
  
    if request.method == 'POST' and request.is_ajax():
        set_form_session_values(request, request.POST)
        return HttpResponse("/locations/event_location/")

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            event = form.save()
            
            (latitude, longitude) = request.session.get('events_selected_coordinates', '46.7667,23.6').split(",")
            event_location = EventLocation()
            event_location.event = event
            event_location.latitude = float(latitude)
            event_location.longitude = float(longitude)
            event_location.save()
            

            if notification:
                notification.send(User.objects.all(), "profiles_new_event", { "event": event }, queue=True)

            request.user.message_set.create(message=_("Event %(event)s has been created.") % {'event':form.cleaned_data["name"]})
        
        cleanup_session_data(request)
        form = form_class()
    else:
        form = form_class(initial=get_initial_form_values_from_session(request))

    return render_to_response(template_name, {
        "form": form,
    }, context_instance = RequestContext(request))


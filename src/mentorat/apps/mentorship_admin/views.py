from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext

from account.utils import get_default_redirect
from signup_codes.models import check_signup_code
from signup_codes.forms import SignupForm, InviteUserForm

from profiles.models import StudentProfile, MentorProfile

@staff_member_required
def admin_profiles(request, template_name="mentorship_admin/admin_search_profiles.html", extra_context=None):
    if extra_context == None:
        extra_context = {}

    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')

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

    return render_to_response(template_name, dict({
        'users': users,
        'order': order,
        'search_terms': search_terms,
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


from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext

from profiles.models import StudentProfile, MentorProfile, FieldOfInterest
from friends.models import FriendshipManager, Friendship
from django.utils.translation import ugettext_lazy as _

from mentoring_agreement.forms import MentoringAgreementForm
from uni_form.helpers import FormHelper, Submit, Reset

def agreements(request, template_name="profiles/agreements.html"):
    friends = Friendship.objects.friends_for_user(request.user)
    users = []
    for f in friends:
        users.append(f['friend'])

    return render_to_response(template_name, dict({
        'friends' : users
    }), context_instance=RequestContext(request))

def agreement(request, username, template_name="profiles/agreement.html"):
    friends = Friendship.objects.friends_for_user(request.user)
    other_user = User.objects.filter(username__iexact=username)
    friendship = None

    if Friendship.objects.are_friends(request.user, other_user) == False:
        raise Http404

    for f in friends:
        if f['friend'].username == username:
            friendship = f['friendship']
            break

    ment_agr = friendship.mentoring_agreement

    initial_dict = {}
    if (len(ment_agr.objectives) == 3):
        initial_dict['objective1'] = ment_agr.objectives[0]
        initial_dict['objective2'] = ment_agr.objectives[1]
        initial_dict['objective3'] = ment_agr.objectives[2]

    if (request.method == 'POST'):
        form = MentoringAgreementForm(request.user.username, username, request.POST)
        if form.is_valid():
            friendship.mentoring_agreement.objectives = [form.cleaned_data['objective1'], form.cleaned_data['objective2'], form.cleaned_data['objective3']]
            friendship.save()
    else:
        form = MentoringAgreementForm(request.user.username, username, auto_id=False, initial=initial_dict)

    helper = FormHelper()

    submit = Submit('save', 'save information')
    helper.add_input(submit)

    return render_to_response(template_name, dict({
        'mentor_form' : form,
        'helper' : helper
    }), context_instance=RequestContext(request))


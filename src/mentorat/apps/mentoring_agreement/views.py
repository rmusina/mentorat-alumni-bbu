from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext

from profiles.models import StudentProfile, MentorProfile, FieldOfInterest
from friends.models import FriendshipManager, Friendship, MentoringAgreement
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
    print ment_agr.objectives

    initial_dict = {}
    if (len(ment_agr.objectives.all()) == 3):
        initial_dict['objective1'] = ment_agr.objectives.all()[0].objective
        initial_dict['objective2'] = ment_agr.objectives.all()[1].objective
        initial_dict['objective3'] = ment_agr.objectives.all()[2].objective
    if (len(ment_agr.communication_methods.all()) == 3):
        initial_dict['communication1'] = ment_agr.communication_methods.all()[0].communication_method
        initial_dict['communication2'] = ment_agr.communication_methods.all()[1].communication_method
        initial_dict['communication3'] = ment_agr.communication_methods.all()[2].communication_method
    if (len(ment_agr.activities.all()) == 3):
        initial_dict['activity1'] = ment_agr.activities.all()[0].activity
        initial_dict['activity2'] = ment_agr.activities.all()[1].activity
        initial_dict['activity3'] = ment_agr.activities.all()[2].activity

    if (request.method == 'POST'):
        form = MentoringAgreementForm(request.user.username, username, request.POST)
        if form.is_valid():
            print form.cleaned_data['objective1']
            friendship.mentoring_agreement.objectives = [form.cleaned_data['objective1'], form.cleaned_data['objective2'], form.cleaned_data['objective3']]
            friendship.mentoring_agreement.communication_methods = [form.cleaned_data['communication1'], form.cleaned_data['communication2'], form.cleaned_data['communication3']]
            friendship.mentoring_agreement.activities = [form.cleaned_data['activity1'], form.cleaned_data['activity2'], form.cleaned_data['activity3']]
            friendship.mentoring_agreement.save()
            friendship.save()
    else:
        form = MentoringAgreementForm(request.user.username, username, initial=initial_dict)

    helper = FormHelper()

    submit = Submit('save', 'save information')
    helper.add_input(submit)

    return render_to_response(template_name, dict({
        'mentor_form' : form,
        'helper' : helper
    }), context_instance=RequestContext(request))


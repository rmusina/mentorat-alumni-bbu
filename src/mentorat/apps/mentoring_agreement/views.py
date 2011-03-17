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

    # if there's no mentoring agreement then create one
    if friendship.mentoring_agreement == None:
        new_ma = MentoringAgreement()
        new_ma.save()
        friendship.mentoring_agreement = new_ma
        friendship.save()
    ment_agr = friendship.mentoring_agreement

    initial_dict = friendship.mentoring_agreement.get_values_as_dict()
    if (request.method == 'POST'):
        form = MentoringAgreementForm(request.POST)
        if form.is_valid():
            friendship.mentoring_agreement.save_from_dict(form.cleaned_data)
            friendship.save()
    else:
        form = MentoringAgreementForm(initial=initial_dict)

    helper = FormHelper()

    submit = Submit('save', 'save information')
    helper.add_input(submit)

    return render_to_response(template_name, dict({
        'mentor_form' : form,
        'helper' : helper
    }), context_instance=RequestContext(request))


from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import models

from account.utils import get_default_redirect
from account.models import OtherServiceInfo
from account.forms import SignupForm, AddEmailForm, LoginForm, \
    ChangePasswordForm, SetPasswordForm, ResetPasswordForm, \
    ChangeTimezoneForm, ChangeLanguageForm, TwitterForm, ResetPasswordKeyForm
from emailconfirmation.models import EmailAddress, EmailConfirmation

association_model = models.get_model('django_openid', 'Association')
if association_model is not None:
    from django_openid.models import UserOpenidAssociation

def login(request, form_class=LoginForm, template_name="account/login.html",
          success_url=None, associate_openid=False, openid_success_url=None,
          url_required=False, extra_context=None):
    if extra_context is None:
        extra_context = {}
    if success_url is None:
        success_url = get_default_redirect(request)
    if request.method == "POST" and not url_required:
        form = form_class(request.POST)
        if form.login(request):
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    ctx = {
        "form": form,
        "url_required": url_required,
    }
    ctx.update(extra_context)
    return render_to_response(template_name, ctx,
        context_instance = RequestContext(request)
    )

def signup(request):
    return render_to_response('account/signup.html', {}, context_instance=RequestContext(request))
    
def signedup(request, email):
    return render_to_response('account/signup_complete.html', {'email': email}, context_instance=RequestContext(request))

@login_required
def password_change(request, form_class=ChangePasswordForm,
        template_name="account/password_change.html"):
    if not request.user.password:
        return HttpResponseRedirect(reverse("acct_passwd_set"))
    if request.method == "POST":
        password_change_form = form_class(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            password_change_form = form_class(request.user)
    else:
        password_change_form = form_class(request.user)
    return render_to_response(template_name, {
        "password_change_form": password_change_form,
    }, context_instance=RequestContext(request))

def password_reset(request, form_class=ResetPasswordForm,
        template_name="account/password_reset.html",
        template_name_done="account/password_reset_done.html"):
    if request.method == "POST":
        password_reset_form = form_class(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.save()
            return render_to_response(template_name_done, {
                "email": email,
            }, context_instance=RequestContext(request))
    else:
        password_reset_form = form_class()
    
    return render_to_response(template_name, {
        "password_reset_form": password_reset_form,
    }, context_instance=RequestContext(request))
    
def password_reset_from_key(request, key, form_class=ResetPasswordKeyForm,
        template_name="account/password_reset_from_key.html"):
    if request.method == "POST":
        password_reset_key_form = form_class(request.POST)
        if password_reset_key_form.is_valid():
            password_reset_key_form.save()
            password_reset_key_form = None
    else:
        password_reset_key_form = form_class(initial={"temp_key": key})
    
    return render_to_response(template_name, {
        "form": password_reset_key_form,
    }, context_instance=RequestContext(request))

@login_required
def language_change(request, form_class=ChangeLanguageForm,
        template_name="account/language_change.html"):
    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
            next = request.META.get('HTTP_REFERER', None)
            return HttpResponseRedirect(next)
    else:
        form = form_class(request.user)
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))

@login_required
def other_services(request, template_name="account/other_services.html"):
    from microblogging.utils import twitter_verify_credentials
    twitter_form = TwitterForm(request.user)
    twitter_authorized = False
    if request.method == "POST":
        twitter_form = TwitterForm(request.user, request.POST)

        if request.POST['actionType'] == 'saveTwitter':
            if twitter_form.is_valid():
                from microblogging.utils import twitter_account_raw
                twitter_account = twitter_account_raw(
                    request.POST['username'], request.POST['password'])
                twitter_authorized = twitter_verify_credentials(
                    twitter_account)
                if not twitter_authorized:
                    request.user.message_set.create(
                        message=ugettext("Twitter authentication failed"))
                else:
                    twitter_form.save()
    else:
        from microblogging.utils import twitter_account_for_user
        twitter_account = twitter_account_for_user(request.user)
        twitter_authorized = twitter_verify_credentials(twitter_account)
        twitter_form = TwitterForm(request.user)
    return render_to_response(template_name, {
        "twitter_form": twitter_form,
        "twitter_authorized": twitter_authorized,
    }, context_instance=RequestContext(request))

@login_required
def other_services_remove(request):
    # TODO: this is a bit coupled.
    OtherServiceInfo.objects.filter(user=request.user).filter(
        Q(key="twitter_user") | Q(key="twitter_password")
    ).delete()
    request.user.message_set.create(message=ugettext("Removed twitter account information successfully."))
    return HttpResponseRedirect(reverse("acct_other_services"))

from django.conf.urls.defaults import *
from account.forms import *
from profiles.forms import *

urlpatterns = patterns('',
    url(r'^login/$', 'account.views.login', name="acct_login"),
    url(r'^password_change/$', 'account.views.password_change', name="acct_passwd"),
    url(r'^password_reset/$', 'account.views.password_reset', name="acct_passwd_reset"),
    url(r'^other_services/$', 'account.views.other_services', name="acct_other_services"),
    url(r'^other_services/remove/$', 'account.views.other_services_remove', name="acct_other_services_remove"),
    
    url(r'^language/$', 'account.views.language_change', name="acct_language_change"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"template_name": "account/logout.html"}, name="acct_logout"),
    
    url(r'^confirm_email/(\w+)/$', 'emailconfirmation.views.confirm_email', name="acct_confirm_email"),

    # Setting the permanent password after getting a key by email
    url(r'^password_reset_key/(\w+)/$', 'account.views.password_reset_from_key', name="acct_passwd_reset_key"),
    
    url(r'^signup/$', 'account.views.signup', name="signup"),
    url(r'^signup/student/$', SignUpWizard([SignupFormForWizard, StudentGeneralInfoForm, StudentEmploymentForm, StudentProfessionalForm, StudentAdditionalForm]), name='signup_student'),
    url(r'^signup/mentor/$', SignUpWizard([SignupFormForWizard, MentorGeneralInfoForm, MentorEmploymentForm, MentorProfessionalForm, MentorAdditionalForm]), name='signup_mentor'),
    url(r'^signedup/(?P<email>.+)/$', 'account.views.signedup', name='signedup'),

    # ajax validation
    (r'^validate/$', 'ajax_validation.views.validate', {'form_class': SignupForm}, 'signup_form_validate'),
)

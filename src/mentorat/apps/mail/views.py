from django.shortcuts import render_to_response
from django.template import RequestContext

import utils, models


def confirm(request, key=''):
    email = utils.check_confirm(key)
    if email is not None:
        return render_to_response('mail/mail_confirmed.html', { 'email': email }, context_instance=RequestContext(request))
    else:
        return render_to_response('mail/mail_confirmed_fail.html', { 'email': email }, context_instance=RequestContext(request))
        

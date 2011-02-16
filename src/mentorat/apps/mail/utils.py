from uuid import uuid1 as UUID
from pinax.core.utils import get_send_mail
send_mail = get_send_mail()
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from models import EmailConfirmation
from django.utils.hashcompat import sha_constructor
from django.core.urlresolvers import reverse

LOG_MAIL = True

def mail(to, subject, message):
    """Send email to user. The mail will be send from the default site email.

    @param to To whom to send the email.
    @param subject The subject of the email.
    @param message The message of the email.
    """
    if LOG_MAIL:
        print '> Sending mail'
        print '> To:', to
        print '> From:', settings.DEFAULT_FROM_EMAIL
        print '>> Subject:', subject
        print '>> Message:', message
        print '< Mail ending'

    send_mail(subject, to, settings.DEFAULT_FROM_EMAIL, [to], priority='high')


def send_mail_confirm(user):
    """Send a confirmation email to the user.
    """
    # Get the profile email
    to = user.get_profile().email
    if EmailConfirmation.objects.filter(email=to).count():
        # see if the email was already confirmed
        confirm = EmailConfirmation.objects.get(email=to)
        if confirm.confirmed:
            return False
        key = confirm.key
    else:
        # generate a unique confirmation key
        key = None
        while not key or EmailConfirmation.objects.filter(key=key).count():
           key = sha_constructor('%s%s' % (to, UUID())).hexdigest()
        confirm = EmailConfirmation(email=to, confirmed=False, key=key)
        confirm.save()

    subject = _('Mail confirmation for mentorat.alumni.ubbcluj.ro')
    message = _("""This message has been sent to you to confirm that you are the owner of the account on mentorat.alumni.ubbcluj.ro at which this email was set.

If the account with username %s belongs to you please click the following link to confirm it:
mentorat.alumni.ubbcluj.ro%s

This message is automatically sent by mentorat.alumni.ubbcluj.ro, please do not repply to this email.""") % (user.username, reverse('email_confirm', kwargs={ 'key' : key }))
    
    mail(to, subject, message)
    
    return True

def check_confirm(key):
    """Check a key if it corresponds to any confirmation email.
    @returns the email of the confirmed key or None if does not exist
    """
    try:
        confirm = EmailConfirmation.objects.get(key=key)
    except EmailConfirmation.DoesNotExist:
        return None
    
    if confirm.confirmed:
        return None

    confirm.confirmed = True
    confirm.key = '--confirmed--'
    confirm.save()
    return confirm.email
    


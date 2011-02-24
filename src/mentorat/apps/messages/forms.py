import datetime
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.contrib.auth.models import User

from pinax.core.utils import get_send_mail
send_mail = get_send_mail()

from profiles.models import StudentProfile, MentorProfile

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from messages.models import Message
from messages.fields import CommaSeparatedUserField

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"))
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))


    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter


    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                subject = subject,
                body = body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = datetime.datetime.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg,})
                    notification.send(recipients, "messages_reply_received", {'message': msg,})
                else:
                    notification.send([sender], "messages_sent", {'message': msg,})
                    notification.send(recipients, "messages_received", {'message': msg,})
        return message_list

class MassComposeForm(forms.Form):
    recipient = CommaSeparatedUserField(label=_(u"Recipient"), required=False)
    subject = forms.CharField(label=_(u"Subject"))
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))
    send_to_email = forms.BooleanField(label=_(u"Send by email (default is private message)"), required=False)
    send_to_students = forms.BooleanField(label=_(u"Send to all active students"), required=False)
    send_to_mentors = forms.BooleanField(label=_(u"Send to all active mentors"), required=False)

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(MassComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        send_to_email = self.cleaned_data['send_to_email']
        send_to_students = self.cleaned_data['send_to_students']
        send_to_mentors = self.cleaned_data['send_to_mentors']

        if isinstance(recipients, str):
            recipients = []

        if send_to_students:
            student_list = [stud.pk for stud in StudentProfile.objects.all()]
            students_as_users = [u for u in User.objects.all().filter(user__profile__pk__in=student_list)]
            recipients.extend(students_as_users)
        if send_to_mentors:
            mentor_list = [ment.pk for ment in MentorProfile.objects.all()]
            mentors_as_users = [u for u in User.objects.all().filter(user__profile__pk__in=mentor_list)]
            recipients.extend(mentors_as_users)

        # filter only unique users
        recipients = list(set(recipients))

        message_list = []

        if send_to_email:
            recipient_emails = [r.get_profile().email for r in recipients]
            for email in recipient_emails:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email], priority="high")
        else:
            for r in recipients:
                msg = Message(
                    sender = sender,
                    recipient = r,
                    subject = subject,
                    body = body,
                )
                if parent_msg is not None:
                    msg.parent_msg = parent_msg
                    parent_msg.replied_at = datetime.datetime.now()
                    parent_msg.save()
                msg.save()
                message_list.append(msg)
                if notification:
                    if parent_msg is not None:
                        notification.send([sender], "messages_replied", {'message': msg,})
                        notification.send(recipients, "messages_reply_received", {'message': msg,})
                    else:
                        notification.send([sender], "messages_sent", {'message': msg,})
                        notification.send(recipients, "messages_received", {'message': msg,})
        return message_list

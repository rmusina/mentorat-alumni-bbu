from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("friends_invite", _("Invitation Received"), _("you have received an invitation"), default=2)
        notification.create_notice_type("friends_invite_sent", _("Invitation Sent"), _("you have sent an invitation"), default=1)
        notification.create_notice_type("friends_accept", _("Acceptance Received"), _("an invitation you sent has been accepted"), default=2)
        notification.create_notice_type("friends_accept_sent", _("Acceptance Sent"), _("you have accepted an invitation you received"), default=1)
        notification.create_notice_type("friends_decline", _("Decline Received"), _("an invitation you sent has been declined"), default=2)
        notification.create_notice_type("friends_decline_sent", _("Decline Sent"), _("you have declined an invitation you received"), default=1)
        notification.create_notice_type("friends_pending", _("Pending Received"), _("an invitation you sent is being considered by a mentor"), default=2)
        notification.create_notice_type("friends_pending_sent", _("Pending Sent"), _("you have accepted to overview an invitation"), default=1)
        notification.create_notice_type("friends_renounce", _("Renounce Received"), _("one student has renounced his application"), default=2)
        notification.create_notice_type("friends_renounce_sent", _("Renounce Sent"), _("you have renounced your application for a mentor"), default=1)
        notification.create_notice_type("join_accept", _("Join Invitation Accepted"), _("an invitation you sent to join this site has been accepted"), default=2)
        notification.create_notice_type("friends_other_mentor", _("User Assigned To Another Mentor"), _("the user who has submitted a request has been assigned to another mentor"), default=2)

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
 
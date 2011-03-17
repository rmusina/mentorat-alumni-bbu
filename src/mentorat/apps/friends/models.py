import datetime
from random import random

from django.db import models
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.hashcompat import sha_constructor
from django.db.models import signals
from django.conf import settings

# favour django-mailer but fall back to django.core.mail
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

if "emailconfirmation" in settings.INSTALLED_APPS:
    from emailconfirmation.models import EmailAddress
else:
    EmailAddress = None

class Contact(models.Model):
    """
    A contact is a person known by a user who may or may not themselves
    be a user.
    """

    # the user who created the contact
    user = models.ForeignKey(User, related_name="contacts")

    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    added = models.DateField(default=datetime.date.today)

    # the user(s) this contact correspond to
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return "%s (%s's contact)" % (self.email, self.user)


class FriendshipManager(models.Manager):

    def friends_for_user(self, user):
        friends = []
        for friendship in self.filter(from_user=user).select_related(depth=1):
            friends.append({"friend": friendship.to_user, "friendship": friendship})
        for friendship in self.filter(to_user=user).select_related(depth=1):
            friends.append({"friend": friendship.from_user, "friendship": friendship})
        return friends

    def are_friends(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count() > 0:
            return True
        if self.filter(from_user=user2, to_user=user1).count() > 0:
            return True
        return False

    def remove(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            friendship = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            friendship = self.filter(from_user=user2, to_user=user1)
        friendship.delete()

class MentoringAgreementObjectives(models.Model):
    description = models.CharField(max_length=200)
    agreement = models.ForeignKey('MentoringAgreement', related_name='objectives')
class MentoringAgreementCommunicationMethods(models.Model):
    description = models.CharField(max_length=200)
    agreement = models.ForeignKey('MentoringAgreement', related_name='communication_methods')
class MentoringAgreementActivites(models.Model):
    description = models.CharField(max_length=200)
    agreement = models.ForeignKey('MentoringAgreement', related_name='activities')
class MentoringAgreementObjectiveGoals(models.Model):
    description = models.CharField(max_length=200)
    agreement = models.ForeignKey('MentoringAgreement', related_name='objective_goals')
class MentoringAgreementProblems(models.Model):
    description = models.CharField(max_length=200)
    agreement = models.ForeignKey('MentoringAgreement', related_name='problems')

class MentoringAgreement(models.Model):
    def get_values_as_dict(self):
        values_dict = {}
        if (len(self.objectives.all()) == 3):
            values_dict['objective1'] = self.objectives.all()[0].description
            values_dict['objective2'] = self.objectives.all()[1].description
            values_dict['objective3'] = self.objectives.all()[2].description
        if (len(self.communication_methods.all()) == 3):
            values_dict['communication1'] = self.communication_methods.all()[0].description
            values_dict['communication2'] = self.communication_methods.all()[1].description
            values_dict['communication3'] = self.communication_methods.all()[2].description
        if (len(self.activities.all()) == 3):
            values_dict['activity1'] = self.activities.all()[0].description
            values_dict['activity2'] = self.activities.all()[1].description
            values_dict['activity3'] = self.activities.all()[2].description
        if (len(self.objective_goals.all()) == 3):
            values_dict['objective_goal1'] = self.objective_goals.all()[0].description
            values_dict['objective_goal2'] = self.objective_goals.all()[1].description
            values_dict['objective_goal3'] = self.objective_goals.all()[2].description
        if (len(self.problems.all()) == 3):
            values_dict['problem1'] = self.problems.all()[0].description
            values_dict['problem2'] = self.problems.all()[1].description
            values_dict['problem3'] = self.problems.all()[2].description
        return values_dict
    def save_from_dict(self, values_dict):
        # Neo: There's got to be a better way then to write code so redundant
        # Morpheus: I'm sorry Neo, it's what the Oracle predicted
        # Zombocom: Welcome to Zombocom
        if (len(self.objectives.all()) == 3):
            self.objectives.all()[0].description = values_dict['objective1']
            self.objectives.all()[1].description = values_dict['objective2']
            self.objectives.all()[2].description = values_dict['objective3']
        else:
            self.objectives.create(description=values_dict['objective1']);
            self.objectives.create(description=values_dict['objective2']);
            self.objectives.create(description=values_dict['objective3']);
        if (len(self.communication_methods.all()) == 3):
            self.communication_methods.all()[0].description = values_dict['communication1']
            self.communication_methods.all()[1].description = values_dict['communication2']
            self.communication_methods.all()[2].description = values_dict['communication3']
        else:
            self.communication_methods.create(description=values_dict['communication1']);
            self.communication_methods.create(description=values_dict['communication2']);
            self.communication_methods.create(description=values_dict['communication3']);
        if (len(self.activities.all()) == 3):
            self.activities.all()[0].description = values_dict['activity1']
            self.activities.all()[1].description = values_dict['activity2']
            self.activities.all()[2].description = values_dict['activity3']
        else:
            self.activities.create(description=values_dict['activity1']);
            self.activities.create(description=values_dict['activity2']);
            self.activities.create(description=values_dict['activity3']);
        if (len(self.objective_goals.all()) == 3):
            self.objective_goals.all()[0].description = values_dict['objective_goal1']
            self.objective_goals.all()[1].description = values_dict['objective_goal2']
            self.objective_goals.all()[2].description = values_dict['objective_goal3']
        else:
            self.objective_goals.create(description=values_dict['objective_goal1']);
            self.objective_goals.create(description=values_dict['objective_goal2']);
            self.objective_goals.create(description=values_dict['objective_goal3']);
        if (len(self.problems.all()) == 3):
            self.problems.all()[0].description = values_dict['problem1']
            self.problems.all()[1].description = values_dict['problem2']
            self.problems.all()[2].description = values_dict['problem3']
        else:
            self.problems.create(description=values_dict['problem1']);
            self.problems.create(description=values_dict['problem2']);
            self.problems.create(description=values_dict['problem3']);
        self.save()

class Friendship(models.Model):
    """
    A friendship is a bi-directional association between two users who
    have both agreed to the association.
    """

    to_user = models.ForeignKey(User, related_name="friends")
    from_user = models.ForeignKey(User, related_name="_unused_")
    # @@@ relationship types
    added = models.DateField(default=datetime.date.today)
    mentoring_agreement = models.OneToOneField('MentoringAgreement', blank=True, null=True, related_name='mentoring_agreement')

    objects = FriendshipManager()

    class Meta:
        unique_together = (('to_user', 'from_user'),)


def friend_set_for(user):
    return set([obj["friend"] for obj in Friendship.objects.friends_for_user(user)])


INVITE_STATUS = (
    ("1", "Created"),
    ("2", "Sent"),
    ("3", "Failed"),
    ("4", "Expired"),
    ("5", "Accepted"),
    ("6", "Declined"),
    ("7", "Joined Independently"),
    ("8", "Deleted"),
    ("9", "Pending"),
    ("10", "Accepted By Other Mentor")
)

class JoinInvitationManager(models.Manager):

    def send_invitation(self, from_user, to_email, message):
        contact, created = Contact.objects.get_or_create(email=to_email, user=from_user)
        salt = sha_constructor(str(random())).hexdigest()[:5]
        confirmation_key = sha_constructor(salt + to_email).hexdigest()

        accept_url = u"http://%s%s" % (
            unicode(Site.objects.get_current()),
            reverse("friends_accept_join", args=(confirmation_key,)),
        )

        ctx = {
            "SITE_NAME": settings.SITE_NAME,
            "CONTACT_EMAIL": settings.CONTACT_EMAIL,
            "user": from_user,
            "message": message,
            "accept_url": accept_url,
        }

        subject = render_to_string("friends/join_invite_subject.txt", ctx)
        email_message = render_to_string("friends/join_invite_message.txt", ctx)

        send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [to_email])
        return self.create(from_user=from_user, contact=contact, message=message, status="2", confirmation_key=confirmation_key)


class JoinInvitation(models.Model):
    """
    A join invite is an invitation to join the site from a user to a
    contact who is not known to be a user.
    """

    from_user = models.ForeignKey(User, related_name="join_from")
    contact = models.ForeignKey(Contact)
    message = models.TextField()
    sent = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=1, choices=INVITE_STATUS)
    confirmation_key = models.CharField(max_length=40)

    objects = JoinInvitationManager()

    def accept(self, new_user):
        # mark invitation accepted
        self.status = "5"
        self.save()
        # auto-create friendship
        friendship = Friendship(to_user=new_user, from_user=self.from_user)
        friendship.save()
        # notify
        if notification:
            notification.send([self.from_user], "join_accept", {"invitation": self, "new_user": new_user})
            friends = []
            for user in friend_set_for(new_user) | friend_set_for(self.from_user):
                if user != new_user and user != self.from_user:
                    friends.append(user)
            notification.send(friends, "friends_otherconnect", {"invitation": self, "to_user": new_user})

class FriendshipInvitationManager(models.Manager):
    def invitations(self, *args, **kwargs):
        return self.filter(*args, **kwargs).exclude(status__in=["6", "8"])

    def invitationsAll(self, *args, **kwargs):
        return self.filter(*args, **kwargs).exclude(status__in=["7", "8"])

    def invitationsDenied(self, *args, **kwargs):
        return self.filter(*args, **kwargs).filter(status="6")

    def otherInvitations(self, *args, **kwargs):
        return self.filter(*args, **kwargs).filter(status="6")

    def sent_invitations(self, *args, **kwargs):
        return self.filter(*args, **kwargs).filter(status="2")

    def hasMentor(self, *args, **kwargs):
        return self.filter(*args, **kwargs).filter(status="5").count() > 0

    def countRequests(self, *args, **kwargs):
        return self.filter(*args, **kwargs).exclude(status__in=["6", "8"]).count()

    def countAccepts(self, *args, **kwargs):
        return self.filter(*args, **kwargs).filter(status="5").count()

class FriendshipInvitation(models.Model):
    """
    A frienship invite is an invitation from one user to another to be
    associated as friends.
    """

    from_user = models.ForeignKey(User, related_name="invitations_from")
    to_user = models.ForeignKey(User, related_name="invitations_to")
    message = models.TextField()
    sent = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=1, choices=INVITE_STATUS)

    objects = FriendshipInvitationManager()

    def accept(self):
        if not Friendship.objects.are_friends(self.to_user, self.from_user):
            friendship = Friendship(to_user=self.to_user, from_user=self.from_user)
            friendship.save()
            self.status = "5"
            self.save()

            #notify other mentors for which the user has applied
            for invitation in FriendshipInvitation.objects.invitations(from_user=self.from_user).exclude(to_user=self.to_user):
                invitation.status = "10"
                invitation.save()
                notification.send([invitation.to_user], "friends_other_mentor", {"invitation": invitation})

            if notification:
                notification.send([self.from_user], "friends_accept", {"invitation": self})
                notification.send([self.to_user], "friends_accept_sent", {"invitation": self})

    def decline(self):
        if not Friendship.objects.are_friends(self.to_user, self.from_user):
            self.status = "6"
            self.save()
            if notification:
                notification.send([self.from_user], "friends_decline", {"invitation": self})
                notification.send([self.to_user], "friends_decline_sent", {"invitation": self})

    def pending(self):
        if not Friendship.objects.are_friends(self.to_user, self.from_user):
            self.status = "9"
            self.save()

            if notification:
                notification.send([self.from_user], "friends_pending", {"invitation": self})
                notification.send([self.to_user], "friends_pending_sent", {"invitation": self})

    def renounce(self):
        if not Friendship.objects.are_friends(self.to_user, self.from_user):
            self.status = "8"
            self.save()

            if notification:
                notification.send([self.to_user], "friends_renounce", {"invitation": self})
                notification.send([self.from_user], "friends_renounce_sent", {"invitation": self})

class FriendshipInvitationHistory(models.Model):
    """
    History for friendship invitations
    """

    from_user = models.ForeignKey(User, related_name="invitations_from_history")
    to_user = models.ForeignKey(User, related_name="invitations_to_history")
    message = models.TextField()
    sent = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=1, choices=INVITE_STATUS)

# @@@ this assumes email-confirmation is being used
def new_user(sender, instance, **kwargs):
    if instance.verified:
        for join_invitation in JoinInvitation.objects.filter(contact__email=instance.email):
            if join_invitation.status not in ["5", "7"]: # if not accepted or already marked as joined independently
                join_invitation.status = "7"
                join_invitation.save()
                # notification will be covered below
        for contact in Contact.objects.filter(email=instance.email):
            contact.users.add(instance.user)
            # @@@ send notification
signals.post_save.connect(new_user, sender=EmailAddress)

if EmailAddress:
    def new_user(sender, instance, **kwargs):
        if instance.verified:
            for join_invitation in JoinInvitation.objects.filter(contact__email=instance.email):
                if join_invitation.status not in ["5", "7"]: # if not accepted or already marked as joined independently
                    join_invitation.status = "7"
                    join_invitation.save()
                    # notification will be covered below
            for contact in Contact.objects.filter(email=instance.email):
                contact.users.add(instance.user)
                # @@@ send notification

    # only if django-email-notification is installed
    signals.post_save.connect(new_user, sender=EmailAddress)

def delete_friendship(sender, instance, **kwargs):
    friendship_invitations = FriendshipInvitation.objects.filter(to_user=instance.to_user, from_user=instance.from_user)
    for friendship_invitation in friendship_invitations:
        if friendship_invitation.status != "8":
            friendship_invitation.status = "8"
            friendship_invitation.save()

signals.pre_delete.connect(delete_friendship, sender=Friendship)

# moves existing friendship invitation from user to user to FriendshipInvitationHistory before saving new invitation
def friendship_invitation(sender, instance, **kwargs):
    friendship_invitations = FriendshipInvitation.objects.filter(to_user=instance.to_user, from_user=instance.from_user)
    for friendship_invitation in friendship_invitations:
        FriendshipInvitationHistory.objects.create(
                from_user=friendship_invitation.from_user,
                to_user=friendship_invitation.to_user,
                message=friendship_invitation.message,
                sent=friendship_invitation.sent,
                status=friendship_invitation.status
                )
        friendship_invitation.delete()

signals.pre_save.connect(friendship_invitation, sender=FriendshipInvitation)

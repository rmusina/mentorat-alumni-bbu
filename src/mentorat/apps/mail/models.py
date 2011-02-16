from django.db import models
from django.contrib.auth.models import User

class EmailConfirmation(models.Model):
    """Confimation email tells us if the user have confimed their email.
    Fields:
        - email = the email of the user
        - confimed = wheter the email was confirmed or not
        - key = confirmation key
    """
    email = models.CharField(max_length=255, null=False, blank=False)

    confirmed = models.BooleanField(null=False, blank=False, default=True)

    key = models.CharField(max_length=255, null=False, blank=False)
    

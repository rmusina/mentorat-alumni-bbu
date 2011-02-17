from django import template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from avatar import AVATAR_DEFAULT_URL, AVATAR_GRAVATAR_BACKUP

register = template.Library()

def show_profile(user):
    return {"user": user}
register.inclusion_tag("profile_item.html")(show_profile)

def clear_search_url(request):
    getvars = request.GET.copy()
    if 'search' in getvars:
        del getvars['search']
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path
register.simple_tag(clear_search_url)

def profile_avatar(user, size=80):
    from django.conf import settings
    import os.path
    if not isinstance(user, User):
        try:
            user = User.objects.get(username=user)
            alt = unicode(user)
            url = ""
            if user.get_profile().as_student() <> None:
                url = os.path.join(settings.STATIC_URL, "student.png")
            else:
                url = os.path.join(settings.STATIC_URL, "mentor.png")
        except User.DoesNotExist:
            url = AVATAR_DEFAULT_URL
            alt = _("Default Avatar")
    else:
        alt = unicode(user)
        url = ""
        user = User.objects.get(username=user)
        if user.is_staff:
            url = os.path.join(settings.STATIC_URL, "img/superuser.png")
        else:
            if user.get_profile().as_student() <> None:
                url = os.path.join(settings.STATIC_URL, "img/student.png")
            else:
                url = os.path.join(settings.STATIC_URL, "img/mentor.png")

    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (url, alt,
        size, size)
register.simple_tag(profile_avatar)

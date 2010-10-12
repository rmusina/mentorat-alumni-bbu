# coding: utf-8

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Admin Site Title
ADMIN_HEADLINE = getattr(settings, "GRAPPELLI_ADMIN_HEADLINE", 'Mentorship admin')
ADMIN_TITLE = getattr(settings, "GRAPPELLI_ADMIN_TITLE", 'Mentorship admin')

# Link to your Main Admin Site (no slashes at start and end)
ADMIN_URL = getattr(settings, "GRAPPELLI_ADMIN_URL", '/admin/')

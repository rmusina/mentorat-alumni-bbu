from django import template
from surveys.models import *

register = template.Library()

@register.filter
def completedSurvey(survey, user):
    return CompletedSurvey.objects.filter(survey=survey, user=user).count() > 0

@register.filter
def for_user(survey, user):
    return (user.is_staff 
            or (user.get_profile().as_student() and survey.for_students) 
            or (user.get_profile().as_mentor() and survey.for_mentors))


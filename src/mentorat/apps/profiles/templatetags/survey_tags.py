from django import template
from surveys.models import *
import random

register = template.Library()

@register.filter
def completedSurvey(survey, user):
    return CompletedSurvey.objects.filter(survey=survey, user=user).count() > 0

@register.filter
def for_user(survey, user):
    return (user.is_staff 
            or (user.get_profile().as_student() and survey.for_students) 
            or (user.get_profile().as_mentor() and survey.for_mentors))

@register.filter
def chart_colors(count, base_color):
    color_string = ''
    R = int(base_color[:2], 16)
    G = int(base_color[2:4], 16)
    B = int(base_color[4:], 16)
    rR = 255 - R
    rG = 255 - G
    rB = 255 - B

    div = 2.0 / 3.0 / (count - 1)

    for i in range(0, count):
        cR = hex(R + int(rR * i * div))[2:]
        cG = hex(G + int(rG * i * div))[2:]
        cB = hex(B + int(rB * i * div))[2:]
        if len(cR) < 2: cR = '0' + cR
        if len(cG) < 2: cG = '0' + cG
        if len(cB) < 2: cB = '0' + cB

        color_string += cR + cG + cB + ',' 
        
    return color_string[:-1]

@register.filter
def chart_step(count):
    return max((count/10, 1))



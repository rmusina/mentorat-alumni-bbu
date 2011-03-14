from django import template

register = template.Library()

@register.filter(name='username_trim')
def username_trim(value, size):
    if len(value) <= size + 3:
        return value
    return value[:size] + '...'

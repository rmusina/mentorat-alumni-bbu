from django.template import Library, Node
from django import template
from profiles.models import *
from profiles.views import AdminEvent

register = Library()

class RecentEventsNode(Node):
    def __init__(self, count, user, name):
        self.count = count
        self.user = template.Variable(user)
        self.name = name
        print count, user, name
        
    def render(self, context):
        user = self.user.resolve(context)
        student = user.get_profile().as_student()
        items = Event.objects.order_by('-date')
        list = []
        for item in items[:self.count]:
            list.append(AdminEvent(item.pk, item.name, 
                                   item.date, item.points, 
                                   StudentEvent.objects.filter(student=student, event=item).count() > 0))
        print self.name, list
        context[self.name] = list
        return ''

# load_recent_events for $user in $varname
@register.tag
def load_recent_events(parser, token):
    content = token.split_contents()
    if len(content) != 6 and content[2] != 'for' and content[4] != 'in':
        raise template.TemplateSyntaxError, 'Invalid use of template tag'
    
    try:
        value = int(content[1])
    except:
        raise template.TemplateSyntaxError, 'First argument must be a number'
    
    if value <= 0:
        raise template.TemplateSyntaxError, 'Count must be positive'
    
    print content
    return RecentEventsNode(value, content[3], content[5])
    
    
    
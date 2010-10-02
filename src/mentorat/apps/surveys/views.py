from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.http import *
from django.template import *
from surveys.forms import *
import re
from django.utils.translation import ugettext_lazy as _

class TextValidator:
    def __init__(self, id, post, verbose=True):
        self.index = id
        self.istext = True
        id = str(id)
        self.valid = True
        self.errors = [ ]
        try:
            self.name = post['field-'+id+'-name'].strip()
        except:
            self.name = ''

        req = 'field-'+id+'-required'
        if req in post  and post[req]=='yes':
            self.required = True
        else:
            self.required = False

        self.validate_name()
        

    def validate_name(self):
        if len(self.name) == 0:
            self.valid = False
            self.errors.append(_('The name of the field cannot be empty'))

    def is_valid(self):
        return self.valid


class BooleanValidator:
    def __init__(self, id, post, verbose=True):
        self.isbool = True
        self.index = id
        id = str(id)
        self.valid = True
        self.errors = [ ]
        try:
            self.name = post['field-'+id+'-name'].strip()
        except:
            self.name = ''

        self.validate_name()
        

    def validate_name(self):
        if len(self.name) == 0:
            self.valid = False
            self.errors.append(_('The name of the field cannot be empty'))

    def is_valid(self):
        return self.valid


class ChoiceValidator:
    def __init__(self, id, post, verbose=True):
        self.ischoice = True
        self.index = id
        id = str(id)
        self.valid = True
        self.errors = [ ]
        try:
            self.name = post['field-'+id+'-name'].strip()
        except:
            self.name = ''

        mchoice = 'field-'+id+'-multichoice'
        if mchoice in post and post[mchoice]=='yes':
            self.multichoice = True
        else:
            self.multichoice = False

        req = 'field-'+id+'-required'
        if req in post  and post[req]=='yes':
            self.required = True
        else:
            self.required = False

        choice = 'field-'+id+'-choices-'
        cid = []
        for field in post.keys():
            match = re.search(choice + r'(\d+)', field)
            if match:
                cid.append(int(match.group(1)))
        cid = sorted(cid)

        self.choices = []
        for id in cid:
            val = post[choice+str(id)].strip()
            if len(val):
                self.choices.append(val)

        self.validate_name()
        self.validate_choices()
        

    def validate_name(self):
        if len(self.name) == 0:
            self.valid = False
            self.errors.append(_('The name of the field cannot be empty'))
        elif len(self.name) >= 255:
            self.valid = False
            self.errors.append(_('The name of the field is too long'))

    def validate_choices(self):
        if len(self.choices) < 2:
            self.valid = False
            self.errors.append(_('The choice set must have at least 2 elements'))


    def is_valid(self):
        return self.valid

def add_survey(request):  
    form = None
    validated = []

    if request.method == 'POST':
        form = AddSurveyForm(request.POST)
        fields = []
        for field in request.POST.keys():
            match = re.search(r'^field-(\d+)-type$', field)
            if match:
                fields.append(int(match.group(1)))

        fields = sorted(fields)
        valid = form.is_valid()

        for (i, id) in enumerate(fields):
            field = 'field-' + str(id) + '-type'
            if request.POST[field] == 'text':
                tmp = TextValidator(id, request.POST)
                tmp.index = i
                validated.append(tmp)
                valid = valid and tmp.is_valid()
            elif request.POST[field] == 'bool':
                tmp = BooleanValidator(id, request.POST)
                tmp.index = i
                validated.append(tmp)
                valid = valid and tmp.is_valid()
            elif request.POST[field] == 'choice':
                tmp = ChoiceValidator(id, request.POST)
                tmp.index = i
                validated.append(tmp)
                valid = valid and tmp.is_valid()
            else:
                pass #not a valid type of field

        if valid:
            raise Exception
    else:
        form = AddSurveyForm()

    return render_to_response('surveys/add.html', { 'form': form, 'fields': validated }, context_instance=RequestContext(request))

def rm_survey(request, id):
    pass 

from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.http import *
from django.template import *
from surveys.forms import *
from surveys.models import *
import re
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list

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

@staff_member_required
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
                print 'Invalid field type:', requst.POST[field]

        if valid:
            survey = form.save()
            for field in validated:
                if isinstance(field, TextValidator):
                    text = TextField()
                    text.index = field.index
                    text.survey = survey
                    text.name = field.name
                    text.required = field.required
                    text.save()
                elif isinstance(field, BooleanValidator):
                    bool = BooleanField()
                    bool.index = field.index
                    bool.survey = survey
                    bool.name = field.name
                    bool.save()
                elif isinstance(field, ChoiceValidator):
                    choice = ChoiceField()
                    choice.index = field.index
                    choice.survey = survey
                    choice.name = field.name
                    choice.multichoice = field.multichoice
                    choice.required = field.required
                    choice.save()
                    for choicename in field.choices:
                        ch = Choice()
                        ch.field = choice
                        ch.name = choicename
                        ch.save()
                else:
                    print 'Invalid field type:', field
            return HttpResponseRedirect(reverse('survey_add_success'))
    else:
        form = AddSurveyForm()

    return render_to_response('surveys/add.html', { 'form': form, 'fields': validated }, context_instance=RequestContext(request))

@staff_member_required
def rm_survey(request, id):
    pass 

@login_required
def survey(request, id):
    survey = get_object_or_404(Survey, pk=id)
    if CompletedSurvey.objects.filter(survey=survey, user=request.user).count() != 0:
        raise Http404
    if request.user.is_staff or (request.user.get_profile().as_student() and not survey.for_students) or (request.user.get_profile().as_mentor() and not survey.for_mentors):
        raise Http404

    if request.method == 'POST':
        form = SurveyForm(survey, request.POST)
        if form.is_valid():
            form.save(survey, request.user)
            return HttpResponseRedirect(reverse('survey_take_success'))
    else:
        form = SurveyForm(survey)

    return render_to_response('surveys/survey_form.html', { 'survey': survey, 'form': form }, context_instance=RequestContext(request))


def user_input_sortkey(object):
    return object.index

class UserInput:
    def __init__(self, name):
        self.name = name
	
    def text(self, text):
        self.isText = True
        self.text = text
	
    def bool(self, checked):
        self.isBool = True
        self.checked = checked

    def choice(self, choice):
        self.isChoice = True
        self.choice = choice

    def mchoice(self, choices):
        self.isMultiChoice = True
        self.choices = choices

    def __unicode__(self):
        ret = self.name + ' '
        if self.isText:
            ret += self.text
        elif self.isBool:
            ret += str(self.checked)
        elif self.isChoice:
            ret += str(self.choice)
        else:
            ret += str(self.choices)
        return ret

    def __str__(self):
        return self.__unicode__



@login_required
def view_user_input(request, id, username):
    if not request.user.is_staff and request.user.username != username:
        raise Http404

    userSurvey = get_object_or_404(CompletedSurvey, survey__pk=id, user__username=username)
    survey = userSurvey.survey
    user = userSurvey.user
	
    fields = []
    for field in TextField.objects.filter(survey=survey):
        fields.append(field)
    for field in BooleanField.objects.filter(survey=survey):
        fields.append(field)
    for field in ChoiceField.objects.filter(survey=survey):
        fields.append(field)

    fields = sorted(fields, key=user_input_sortkey)

    userInput = []
    for field in fields:
        answer = None
        if isinstance(field, TextField):
            input = TextFieldAnswer.objects.filter(user=user, field=field)
            if input.count():
                answer = UserInput(field.name)
                answer.text(input[0].answer)
        elif isinstance(field, BooleanField):
            input = BooleanFieldAnswer.objects.filter(user=user, field=field)
            answer = UserInput(field.name)
            answer.bool(input.count() > 0)
        elif isinstance(field, ChoiceField):
            choices = UserChoice.objects.filter(choice__field=field, user=user)
            if choices.count():
                answer = UserInput(field.name)
                if not field.multichoice:
                    answer.choice(choices[0].choice.name)
                else:
                    choice_names = []
                    for x in choices:
                        choice_names.append(x.choice.name)
                    answer.mchoice(choice_names)
        if answer != None:
            userInput.append(answer)

    return render_to_response('surveys/view_user_input.html', 
                              { 'other_user': user, 'survey': survey, 'inputs': userInput }, 
                              context_instance=RequestContext(request))

@login_required
def survey_list(request, *args, **kargs):
    kargs['queryset'] = Survey.objects.all().order_by('-created')
    kargs['paginate_by'] = 50
    kargs['template_name'] = 'surveys/survey_list.html'

    return object_list(request, *args, **kargs)
    
@staff_member_required
def stats(request, id):
    survey = get_object_or_404(Survey, pk=id)

    return render_to_response('surveys/survey_stats.html', { 'survey': survey }, context_instance=RequestContext(request))

@staff_member_required
def stats_userlist(request, *args, **kargs):
    id = kargs['id']
    kargs.pop('id')
    survey = get_object_or_404(Survey, pk=id)

    kargs['queryset'] = CompletedSurvey.objects.filter(survey=survey).order_by('-date')
    kargs['paginate_by'] = 50
    kargs['template_name'] = 'surveys/survey_stats_users.html'
    kargs['extra_context'] = { 'survey': survey }

    return object_list(request, *args, **kargs)

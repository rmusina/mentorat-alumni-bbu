from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.http import *
from django.template import *
from surveys.forms import *

def add_survey(request):  
    form = None

    if request.method == 'POST':
        form = AddSurveyForm(request.POST)
    else:
        form = AddSurveyForm()

    return render_to_response('surveys/add.html', { 'form' : form }, context_instance=RequestContext(request))

def rm_survey(request, id):
    pass 

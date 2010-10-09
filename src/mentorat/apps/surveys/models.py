from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Survey(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name=_('survey name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    for_students = models.BooleanField(default=True, verbose_name=_('student survey'))
    for_mentors = models.BooleanField(default=False, verbose_name=_('mentor survey'))
    created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class BaseField(models.Model):
    index = models.IntegerField()
    survey = models.ForeignKey(Survey)
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return str(self.survey) + ': ' + self.name

    class Meta:
        abstract = True


class TextField(BaseField):
    required = models.BooleanField(default=True)


class BooleanField(BaseField):
    pass


class ChoiceField(BaseField):
    multichoice = models.BooleanField(default=False)
    required = models.BooleanField(default=True)


class Choice(models.Model):
    field = models.ForeignKey(ChoiceField)
    name = models.TextField()

    def __unicode__(self):
        return self.name


class TextFieldAnswer(models.Model):
    field = models.ForeignKey(TextField)
    user = models.ForeignKey(User)
    answer = models.TextField()

    def __unicode__(self):
        return '%s (%s): %s' % (self.user.username, self.field.name, self.answer)


class BooleanFieldAnswer(models.Model):
    field = models.ForeignKey(BooleanField)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '%s - %s' % (self.user.username, self.field.name)


class UserChoice(models.Model):
    choice = models.ForeignKey(Choice)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '%s - %s (%s)' % (self.user.username, self.choice.name, self.choice.field.name)


class CompletedSurvey(models.Model):
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - %s' % (self.user.username, str(self.survey))


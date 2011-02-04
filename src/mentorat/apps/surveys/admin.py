from django.contrib import admin
from surveys.models import *
from django.utils.translation import ugettext_lazy as _

class TextInline(admin.TabularInline):
    model = TextField

class BooleanInline(admin.TabularInline):
    model = BooleanField

class ChoiceInline(admin.TabularInline):
    model = Choice

class ChoicesInline(admin.TabularInline):
    model = ChoiceField
    inlines = [ ChoiceInline ]

class SurveyAdmin(admin.ModelAdmin):
    inlines = [ TextInline, BooleanInline, ChoicesInline ]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Choice)
admin.site.register(TextFieldAnswer)
admin.site.register(BooleanFieldAnswer)
admin.site.register(UserChoice)
admin.site.register(CompletedSurvey)


from django.contrib import admin
from friends.models import Contact, Friendship, JoinInvitation, \
                           FriendshipInvitation, FriendshipInvitationHistory, MentoringAgreement, \
                           MentoringAgreementObjectives, MentoringAgreementCommunicationMethods, MentoringAgreementActivites, \
                           MentoringAgreementProblems, MentoringAgreementObjectiveGoals

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user', 'added')

class FriendshipMentoringAgreementInline(admin.TabularInline):
    model = MentoringAgreement

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'added',)
    inlines = [
        FriendshipMentoringAgreementInline,
    ]

class JoinInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'contact', 'status')

class FriendshipInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'sent', 'status',)

class FriendshipInvitationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'sent', 'status',)

class MentoringAgreementObjectivesInline(admin.TabularInline):
    model = MentoringAgreementObjectives

class MentoringAgreementCommunicationMethodsInline(admin.TabularInline):
    model = MentoringAgreementCommunicationMethods

class MentoringAgreementProblemsInline(admin.TabularInline):
    model = MentoringAgreementProblems

class MentoringAgreementActivitesInline(admin.TabularInline):
    model = MentoringAgreementActivites

class MentoringAgreementObjectiveGoalsInline(admin.TabularInline):
    model = MentoringAgreementObjectiveGoals

class MentoringAgreementAdmin(admin.ModelAdmin):
    inlines = [
        MentoringAgreementObjectivesInline,
        MentoringAgreementCommunicationMethodsInline,
        MentoringAgreementActivitesInline,
        MentoringAgreementObjectiveGoalsInline,
        MentoringAgreementProblemsInline,
    ]


admin.site.register(Contact, ContactAdmin)
admin.site.register(MentoringAgreement, MentoringAgreementAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(JoinInvitation, JoinInvitationAdmin)
admin.site.register(FriendshipInvitation, FriendshipInvitationAdmin)
admin.site.register(FriendshipInvitationHistory, FriendshipInvitationHistoryAdmin)
admin.site.register(MentoringAgreementObjectives)
admin.site.register(MentoringAgreementCommunicationMethods)
admin.site.register(MentoringAgreementActivites)
admin.site.register(MentoringAgreementObjectiveGoals)
admin.site.register(MentoringAgreementProblems)

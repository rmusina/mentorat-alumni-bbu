from django.contrib import admin
from friends.models import Contact, Friendship, JoinInvitation, \
                           FriendshipInvitation, FriendshipInvitationHistory, MentoringAgreement, \
                           MentoringAgreementObjectives, MentoringAgreementCommunicationMethods, MentoringAgreementActivites, \
                           MentoringAgreementProblems, MentoringAgreementObjectiveGoals

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user', 'added')

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'added',)

class JoinInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'contact', 'status')

class FriendshipInvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'sent', 'status',)

class FriendshipInvitationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'sent', 'status',)

class MentoringAgreementObjectivesInline(admin.TabularInline):
    model = MentoringAgreementObjectives
    extra = 0

class MentoringAgreementCommunicationMethodsInline(admin.TabularInline):
    model = MentoringAgreementCommunicationMethods
    extra = 0

class MentoringAgreementProblemsInline(admin.TabularInline):
    model = MentoringAgreementProblems
    extra = 0

class MentoringAgreementActivitesInline(admin.TabularInline):
    model = MentoringAgreementActivites
    extra = 0

class MentoringAgreementObjectiveGoalsInline(admin.TabularInline):
    model = MentoringAgreementObjectiveGoals
    extra = 0

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

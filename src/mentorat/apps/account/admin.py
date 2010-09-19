from django.contrib import admin
from django.contrib.auth.models import User
from account.models import Account, OtherServiceInfo, PasswordReset
from profiles.models import Profile

admin.site.register(OtherServiceInfo)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'language')

class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'temp_key', 'timestamp', 'reset')

admin.site.register(PasswordReset, PasswordResetAdmin)
admin.site.register(Account, AccountAdmin)


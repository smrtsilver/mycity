from profile import Profile

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from accounts.models import profile, sms


# admin.site.register(profile)
# admin.site.register(sms)
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = profile
    def has_delete_permission(self, request, obj=None):
        return False

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)

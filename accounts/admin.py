

from django.contrib import admin

# Register your models here.
from accounts.models import profile, sms


admin.site.register(profile)
# admin.site.register(sms)


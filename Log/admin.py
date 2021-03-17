from django.contrib import admin

# Register your models here.
# from Log.models import log_action
# from Log.models import VersionModel
#
# admin.site.register(VersionModel)
from Log.models import FeedbackModel

admin.site.register(FeedbackModel)
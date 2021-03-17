from django.contrib import admin

# Register your models here.
# from Log.models import log_action
# from Log.models import VersionModel
#
# admin.site.register(VersionModel)
from nested_admin.nested import NestedModelAdmin

from Log.models import FeedbackModel


class feedbackAdmin(NestedModelAdmin):
    readonly_fields = [
        "description",
        "user_connect",
        'createtime',

    ]
    ordering = ['-date_time']
    # list_filter = ("valid","group")
    list_filter = [
        "status"
        # ('create_time', DateFieldListFilter)
    ]


    def createtime(self, obj):
        return obj.get_date()

    createtime.short_description = "زمان ثبت"

admin.site.register(FeedbackModel,feedbackAdmin)
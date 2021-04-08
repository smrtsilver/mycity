from django.contrib import admin

# Register your models here.
from nested_admin.nested import NestedModelAdmin

from shop.models import payment



class PaymentAdmin(NestedModelAdmin):
    # class Media:
    #     css = {
    #         'all': ('/static/admin/css/extracss.css',)
    #     }
    # list_display = ['title', 'valid', "group", "view", "call"]
    # exclude = ("author",)
    ordering = ["-create_time"]
    # list_filter = ("valid","group")
    readonly_fields = [
        "receipt",
    "userpayment",

    "status",
    "totalpayment",
    "desc",
    "create_time",
    ]
    list_filter = [
        "status",
    ]
admin.site.register(payment,PaymentAdmin)
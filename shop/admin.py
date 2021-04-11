from django.contrib import admin

# Register your models here.
from nested_admin.nested import NestedModelAdmin

from shop.models import paymentModel



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

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(paymentModel,PaymentAdmin)
from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter
from django.db.models import Count
from django.utils.html import format_html
from django.utils.translation import ngettext
from django_jalali.admin.filters import JDateFieldListFilter

from content.models import *
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

# admin.site.register(base_content)
admin.site.register(group)
# admin.site.register(tariff)
# admin.site.register(city_prob)
# admin.site.register(Image)
# admin.site.register(employment)
# admin.site.register(platform)
# admin.site.register(Comment)
# admin.site.register(like)
# admin.site.register(bookmark)
# admin.site.register(sub_group)
# def make_published(modeladmin, request, queryset):
#     queryset.update(status='p')
# make_published.short_description = "Mark selected stories as published"
admin.site.register(citymodel)


# admin.site.register(platformModel)

class tabsareInline(NestedTabularInline):
    model = TariffOptionsModel
    extra = 1


class tariffModelInline(admin.ModelAdmin):
    model = tariffModel
    extra = 1
    inlines = [tabsareInline, ]


class ImageInline(NestedTabularInline):
    model = Image
    extra = 1
    fields = ('image', "image_tag", "mainpic",)
    readonly_fields = ('image_tag',)
    radio_fields = {'mainpic': admin.VERTICAL}

    # readonly_fields = ['mainpic']
    def image_tag(self, obj):
        return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))

    image_tag.short_description = 'تصویر'


class albumInlineInline(NestedTabularInline):
    model = ImageAlbum
    extra = 1
    inlines = [ImageInline, ]

    def has_delete_permission(self, request, obj=None):
        return False


class validfilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('بر اساس وضعیت')

    parameter_name = 'valid'

    def lookups(self, request, model_admin):
        return (
            (1, "تایید شده"),
            (2, "تایید نشده"),
            (3, "درحال بررسی"),

        )

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(valid__exact=1)
        elif self.value() == "2":
            return queryset.filter(valid__exact=2)
        elif self.value() == "3":
            return queryset.filter(valid__exact=3)


class expiretimefilter(admin.SimpleListFilter):
    title = ('بر اساس تاريخ انقضا')

    parameter_name = 'expire'

    def lookups(self, request, model_admin):
        return (
            (1, "منقضی شده"),
            (2, "مهلت دار"),
        )

    def queryset(self, request, queryset):
        if self.value() == "1":
            # jmodels.timezone.now() + datetime.timedelta(seconds=10)
            return queryset.filter(expiretime__lt=jmodels.timezone.now())
        elif self.value() == "2":
            return queryset.filter(expiretime__gte=jmodels.timezone.now())


# you need import this for adding jalali calander widget

class BarAdmin(admin.ModelAdmin):
    list_filter = (
        ('date', JDateFieldListFilter),
    )


class BarTimeAdmin(admin.ModelAdmin):
    list_filter = (
        ('expiretime', JDateFieldListFilter),
    )


class basecontentAdmin(NestedModelAdmin):
    # class Media:
    #     css = {
    #         'all': ('/static/admin/css/extracss.css',)
    #     }
    inlines = [albumInlineInline, ]
    list_display = ['title', 'valid', "group", "view", "call"]
    exclude = ("author",)
    ordering = ['valid', "-create_time"]
    # list_filter = ("valid","group")
    list_filter = [
        "city",
        ('expiretime', JDateFieldListFilter),

        # ('create_time', DateFieldListFilter)
    ]

    # actions = ['']

    # actions = ["delete_model"]

    def delete_queryset(self, request, queryset):
        n = queryset.count()
        if n:
            for obj in queryset:
                obj.valid = 4
                obj.save()
                # messages.SUCCESS(request,"hhhhhhhh")
            # self.message_user(request, ngettext(
            #     '%d story was successfully marked as published.',
            #     '%d stories were successfully marked as published.',
            #     n,
            # ) % n, messages.SUCCESS)
            # self.message_user(request, (f"تعداد {n} آگهی حذف شدند"), messages.SUCCESS)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'valid':
            kwargs['choices'] = (
                (1, "تایید شده"),
                (2, "تایید نشده"),
                (3, "درحال بررسی"),
            )
            # if request.user.is_superuser:
            #     kwargs['choices'] += (('ready', 'Ready for deployment'),)
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            groups = [g.id for g in request.user.groups.all()]
            if db_field.name == "group":
                if 1 in groups:
                    # cat = request.user.principal.school
                    kwargs['queryset'] = group.objects.filter(id__exact=1)
                    # if request.user.groups.filter(id=1).exists():
                if 2 in groups:
                    kwargs['queryset'] = group.objects.filter(id__exact=7)
                    #     form.base_fields["group"].disabled = True
                    #     form.base_fields['group'].initial = 1
                    # elif request.user.groups.filter(id=2).exists():
                    #     form.base_fields["group"].disabled = True
                    #     form.base_fields['group'].initial = 7
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def delete_model(modeladmin, request, queryset):
        # from collections.abc import Iterable
        # if isinstance(queryset, Iterable):
        #     for obj in queryset:
        #         obj.NOTSHOW=True
        #         obj.save()
        # else:
        queryset.valid = 4
        queryset.save()

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter = [
                "city",
                expiretimefilter,

                # ('create_time', DateFieldListFilter)
            ]
            self.list_filter.extend([validfilter])
            self.list_filter.extend(["group"])

        return super(basecontentAdmin, self).changelist_view(request, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        form.base_fields['phonenumber'].initial = request.user.username
        if not is_superuser:
            form.base_fields['phonenumber'].disabled = True

        form.base_fields['tariff'].help_text = "برای انتخاب چند آگهی کلید ctrl را فشار دهید و سپس انتخاب کنید"

        return form

    readonly_fields = [
        'createtime',
        "timevalid"
    ]

    def timevalid(self, obj):

        year = obj.validtime.date().year
        day = obj.validtime.date().day
        month = obj.validtime.date().month
        date = f"{year}/{day}/{month}"

        hour = obj.validtime.time().hour
        minute = obj.validtime.time().minute
        second = obj.validtime.time().second
        time = f"{hour}:{minute}:{second}"

        return f"{date}  {time}"

    timevalid.short_description = "زمان تاييد"

    def createtime(self, obj):
        time = obj.get_time()
        date = obj.get_date()
        return f"{date}  {time}"

    createtime.short_description = "زمان ثبت"

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if getattr(obj, 'user', None) is None:
                obj.author = request.user.userprofile
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.exclude(valid=4)
        return qs.filter(author=request.user.userprofile).exclude(valid=4)

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         call=Count('call')
    #     )
    #     return queryset
    #
    # def get_device_number(self, obj):
    #     return obj.call
    #
    # get_device_number.admin_order_field = 'call'

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         _hero_count=Count(self.log_content, distinct=True),
    #         # _villain_count=Count("view", distinct=True),

    #     )
    #     return queryset
    #
    # def hero_count(self, obj):
    #     return obj.call
    #
    # def villain_count(self, obj):
    #     return obj.view
    #
    # hero_count.admin_order_field = '_hero_count'
    # villain_count.admin_order_field = '_villain_count'
    # def call(self, obj):
    #     return obj.call
    #
    # call.admin_order_field = 'call'


admin.site.register(base_content, basecontentAdmin)
admin.site.register(tariffModel, tariffModelInline)
# class albumInline(admin.TabularInline):
#     model = ImageAlbum
# class ImageInline(admin.TabularInline):
#     model=Image
# class base_contentAdmin(admin.ModelAdmin):
#     list_display = ['title', 'valid',"group","view","call","get_Image"]
#     ordering = ['valid']
#     # readonly_fields = ['get_Image']
#     # #
#     # def get_Image(self, ImageAlbum):
#     #     d=[]
#     #     a=ImageAlbum.modelAlbum.imagesA.all()
#     #     for i in a:
#     #         d.append(i.image.url)
#
#     inlines = [
#         albumInline,
#     ]
# class albumadmin(admin.ModelAdmin):
#     inlines = [
#         ImageInline,
#     ]
#
#     # actions = [make_published]
# admin.site.register(base_content, base_contentAdmin)
# admin.site.register(ImageAlbum,albumadmin)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('blogpost_connected', 'created_time',"approved_comment")
#     list_filter = ('approved_comment', 'created_time')
#     search_fields = ('text',)
#     actions = ['approve_comments']
#
#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)

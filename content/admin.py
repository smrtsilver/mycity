from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from content.models import *
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline

# admin.site.register(base_content)
# admin.site.register(group)
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


class ImageInline(NestedTabularInline):
    model = Image
    extra = 1
    fields = ('image',"image_tag","mainpic",)
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
class basecontentAdmin(NestedModelAdmin):
    # class Media:
    #     css = {
    #         'all': ('/static/admin/css/extracss.css',)
    #     }
    inlines = [albumInlineInline, ]
    list_display = ['title', 'valid', "group", "view", "call"]
    exclude = ("NOTSHOW","author")
    ordering = ['valid',"-create_time"]
    # list_filter = ("valid","group")
    list_filter = [
        "city",
    ]

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_filter=[
                    "city",
                        ]
            self.list_filter.extend(["valid"])
            self.list_filter.extend(["group"])

        return super(basecontentAdmin, self).changelist_view(request, extra_context)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        form.base_fields['phonenumber'].initial = request.user.username
        if not is_superuser:
            form.base_fields['phonenumber'].disabled = True

            if request.user.groups.filter(id=1).exists():
                form.base_fields["group"].disabled = True
                form.base_fields['group'].initial = 1

        return form

    readonly_fields = [
        'createtime',
    ]

    def createtime(self,obj):
        time=obj.get_time()
        date=obj.get_date()
        return f"{date}  {time}"
    createtime.short_description = "زمان ثبت"

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.author = request.user.userprofile
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user.userprofile)

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

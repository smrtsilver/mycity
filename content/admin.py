from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from content.models import *

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
from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class ImageInline(NestedTabularInline):
    model = Image
    extra = 1
    fields = ('image',"image_tag","mainpic",)
    readonly_fields = ('image_tag',)
    radio_fields = {'mainpic': admin.VERTICAL}
    # readonly_fields = ['mainpic']
    def image_tag(self, obj):
        return format_html('<img src="{}" width="150" height="150"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

class albumInlineInline(NestedTabularInline):
    model = ImageAlbum
    extra = 1
    inlines = [ImageInline, ]

class basecontentAdmin(NestedModelAdmin):
    inlines = [albumInlineInline, ]
    list_display = ['title', 'valid', "group", "view", "call"]
    ordering = ['valid',"-create_time"]


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

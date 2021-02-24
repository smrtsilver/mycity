from django.contrib import admin

# Register your models here.
from content.models import *

# admin.site.register(base_content)
# admin.site.register(group)
# admin.site.register(tariff)
# admin.site.register(city_prob)

admin.site.register(Image)
# admin.site.register(employment)
# admin.site.register(platform)
# admin.site.register(Comment)
admin.site.register(like)
admin.site.register(citymodel)
admin.site.register(bookmark)

# admin.site.register(sub_group)
# def make_published(modeladmin, request, queryset):
#     queryset.update(status='p')
# make_published.short_description = "Mark selected stories as published"
class albumInline(admin.TabularInline):
    model = ImageAlbum
class ImageInline(admin.TabularInline):
    model=Image
class base_contentAdmin(admin.ModelAdmin):
    list_display = ['title', 'valid',"group"]
    ordering = ['valid']
    inlines = [
        albumInline,
    ]
class albumadmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    # actions = [make_published]
admin.site.register(base_content, base_contentAdmin)
admin.site.register(ImageAlbum,albumadmin)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('blogpost_connected', 'created_time',"approved_comment")
#     list_filter = ('approved_comment', 'created_time')
#     search_fields = ('text',)
#     actions = ['approve_comments']
#
#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)

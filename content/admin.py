from django.contrib import admin

# Register your models here.
from content.models import *

admin.site.register(content)
admin.site.register(group)
admin.site.register(tariff)
admin.site.register(city_prob)
# admin.site.register(ImageAlbum)
admin.site.register(Image)
admin.site.register(employment)
admin.site.register(platform)
admin.site.register(Comment)
# admin.site.register(sub_group)

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('blogpost_connected', 'created_time',"approved_comment")
#     list_filter = ('approved_comment', 'created_time')
#     search_fields = ('text',)
#     actions = ['approve_comments']
#
#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)

from django.contrib import admin

# Register your models here.
from content.models import content, group

admin.site.register(content)
admin.site.register(group)
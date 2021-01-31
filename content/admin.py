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
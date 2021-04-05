from django.core.management.base import BaseCommand

from django_jalali.db import models as jmodels

from content.models import base_content


class Command(BaseCommand):
     help = 'tariff update'
     def handle(self, *args, **kwargs):
         expire=base_content.objects.filter(expiretime__lt=jmodels.timezone.now()).update(valid=4)

         objs=base_content.objects.filter(tariff__platform=1, valid=True)
         for obj in objs:
             tarefe=obj.tariff.get(platform=1)
             if obj.startshowtime.togregorian()+tarefe.time>jmodels.timezone.now():
                 obj.startshowtime = obj.startshowtime + tarefe.time
                 obj.save()









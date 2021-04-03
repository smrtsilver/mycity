from django.core.management.base import BaseCommand
from django_jalali.db import models as jmodels
class Command(BaseCommand):
     help = 'Displays current time'
     def handle(self, *args, **kwargs):
         time = jmodels.timezone.now().strftime('%X')
         self.stdout.write("It's now %s" % time)
from django.db import models
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class profile(models.Model):
    phonenumber=models.ForeignKey(User,on_delete=models.PROTECT)
    city=models.CharField(max_length=30)


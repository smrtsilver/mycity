import pyotp
from django.db import models

from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class profile(models.Model):
    phonenumber = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)


class sms(models.Model):
    # methods
    phonenumber = models.CharField(max_length=15)
    key = models.CharField(max_length=100, unique=True,blank=True)
    verified = models.BooleanField(default=False, blank=True, null=True)

    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here we are using Time Based OTP. The interval is 300 seconds.
        # otp must be provided within this interval or it's invalid
        t = pyotp.TOTP(self.key, interval=500)
        return t.verify(provided_otp)

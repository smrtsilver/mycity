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
    #Todo folderbandi
    profile_image=models.ImageField(upload_to="profile",default="1.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userprofile")
    city = models.CharField(max_length=30)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            profile.objects.create(user=instance)
        instance.userprofile.save()

    def __str__(self):
        return self.user.username


class sms(models.Model):
    # methods
    phonenumber = models.CharField(max_length=15)
    key = models.CharField(max_length=100, unique=True, blank=True)
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
        t = pyotp.TOTP(self.key, interval=120)
        return t.verify(provided_otp)

    def __str__(self):
        return self.phonenumber

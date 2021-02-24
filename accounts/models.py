import pyotp
from django.db import models

from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    # model = instance.content.__class__._meta
    username=instance.user.username
    return f'profile/{username}/{filename}'
# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class profile(models.Model):
    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربر"
    #Todo folderbandi
    profile_image=models.ImageField(verbose_name="تصویر کاربر",upload_to=get_upload_path,default="1.jpg")
    user = models.OneToOneField(User, verbose_name="اکانت کاربر",on_delete=models.CASCADE,related_name="userprofile")
    city = models.CharField(verbose_name="شهر کاربر",max_length=30)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            profile.objects.create(user=instance)
        instance.userprofile.save()


    def __str__(self):
        return self.user.username


class sms(models.Model):
    # methods
    class Meta:
        verbose_name="پیامک"
        verbose_name_plural="پیامک"
    phonenumber = models.CharField(verbose_name="شماره تلفن",max_length=15)
    key = models.CharField(verbose_name="کد ارسالی",max_length=100, unique=True, blank=True)
    verified = models.BooleanField(verbose_name="تایید شده",default=False, blank=True, null=True)

    def authenticate(self, otp):
        """ This method authenticates the given otp"""
        provided_otp = 0
        try:
            provided_otp = int(otp)
        except:
            return False
        # Here we are using Time Based OTP. The interval is 300 seconds.
        # otp must be provided within this interval or it's invalid
        # t = pyotp.TOTP(self.key, interval=60)
        if self.key == otp:
        # return t.verify(provided_otp)
            self.key=True
            return True
        else:
            self.key=False
            return False

    def __str__(self):
        return self.phonenumber

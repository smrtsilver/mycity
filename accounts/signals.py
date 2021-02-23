import string

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from accounts.models import sms
import pyotp
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
       return ''.join(random.choice(chars) for _ in range(size))
# def generate_key():
#     """ User otp key generator """
#     key = pyotp.random_base32()
#     if is_unique(key):
#         return key
#     generate_key()
#
#
# def is_unique(key):
#     try:
#         sms.objects.get(key=key)
#     except sms.DoesNotExist:
#         return True
#     return False


@receiver(pre_save, sender=sms)
def create_key(sender, instance, **kwargs):
    """This creates the key for users that don't have keys"""
    if not instance.key:
        instance.key = id_generator(4,"123456789")
    else:
        instance.key = id_generator(4,"123456789")



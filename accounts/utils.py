import pyotp
from rest_framework.response import Response
from accounts.models import sms


def sendsmsmethod(number, format=None):

        try:
            data = int(number)
            a = sms.objects.update_or_create(phonenumber=data)
            time_otp = pyotp.TOTP(a[0].key, interval=60)
            time_otp = time_otp.now()

        except Exception as e:
            content = {
                "message": e,
                "success" : False
            }
            return content
        else:
            content = {
                "message": "کد تایید شما در نرم افزار {} می باشد".format(time_otp),
                "success": True
            }
            return content

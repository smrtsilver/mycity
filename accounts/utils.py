import pyotp
from rest_framework.response import Response
from accounts.models import sms


def sendsmsmethod(number, format=None):

        try:

            data = number
            a = sms.objects.get_or_create(phonenumber=data)
            print(a,a[0].key)
            time_otp = pyotp.TOTP(a[0].key, interval=120)
            print(time_otp)
            time_otp = time_otp.now()
            print(time_otp)

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

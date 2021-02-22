import pyotp
import requests
from rest_framework.response import Response
from accounts.models import sms


def sendsmsmethod(number, format=None):
    try:

        # data = number
        a = sms.objects.get_or_create(phonenumber=number)
        # print(a,a[0].key)
        # time_otp = pyotp.TOTP(a[0].key, interval=1110)
        time_otp = a[0].key
        # print(time_otp)
        # time_otp = time_otp.now()
        # print(time_otp)
        # time_otp = pyotp.TOTP(request.user.key, interval=300)
        # time_otp = time_otp.now()
    except Exception as e:
        content = {
            "message": e,
            "success": False
        }
        return content
    else:
        re = smspanel(number, time_otp)
        content = {
            "message": "کد تایید شما در نرم افزار {} می باشد".format(time_otp),
            "success": True,
            "smssend": re
        }
        smspanel(number, time_otp)
        return content


def smspanel(number, smscode):
    baseUrl = "http://185.112.33.62/api/v1/rest/sms/send"
    custom_header = {"token": "4f7336e638aeb01b4e2c778923ee35e3a8e662c4"}
    json = {"from": "2000198", "recipients": [f"{number}"], "message": f"{smscode}","authcode":smscode, "type": 0, "patternID": 116}
    request = requests.post(baseUrl,
                            json=json,headers=custom_header)
    json = request.json()
    if (json):
        return json
    else:
        print("Response error")
        return 0

import pyotp
import requests
from rest_framework.response import Response
from accounts.models import sms
import re


def sendsmsmethod(number, format=None):

        a = sms.objects.update_or_create(phonenumber=number)
        time_otp = a[0].key
        re = smspanel(number, time_otp)
        content = {
            "message": "کد تایید شما در نرم افزار {} می باشد".format(time_otp),
            "success": True,
            "smssend": re
        }
        # smspanel(number, time_otp)
        return content


def smspanel(number, smscode):
    data=re.match(r'^09(3|0)[0-9]{8}$',number)

    baseUrl = "http://185.112.33.62/api/v1/rest/sms/send"
    custom_header = {"token": "b93502c9d8661db7a3ee956220e439d12f5d2d43"}
    kh_num="90003561"
    omo_num="10001000000321"
    message=f"کد تایید شما در برنامه شهر من : {smscode}"
    basejson = {"from": kh_num,"recipients":[number,],"message":message,"type":0}
    if data:
        basejson["from"]=omo_num
    else:
        basejson["from"]=kh_num
    request = requests.post(baseUrl, json=basejson, headers=custom_header)
    json = request.json()
    if (json):
        return json
    else:
        print("Response error")
        return 0

from rest_framework.views import APIView
import pyotp
from django.contrib.auth import authenticate
from rest_framework import status
# from rest_framework.authtoken.admin import User
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated  # <-- Here
# import requests
# new_token = Token.objects.create(user=request.user)
from accounts.models import sms
from accounts.serializers import *
from accounts.utils import sendsmsmethod

# Create your views here.
from content.serializers import *


class createcategory(APIView):
    def post(self, request):
        # data=request.data
        # ser=groupserializers(data=data)
        # if ser.is_valid():
        #     pass
        # else:
        #     content={
        #         "message" : "ورودی ها صحیح نیستند"
        #     }
        pass


class createcontent(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        ser = contentserializers(data=data)
        if ser.is_valid():
            try:
                ser.save()
            except Exception as e:
                content = {
                    "message": "بروز خطا",
                    "created": False,
                    "errors": e
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:

                content = {
                    "message": "اگهی ایجاد شد",
                    "created": True,

                }
                return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {
                "message": "داده های ارسالی صحیح نیستند",
                "created": False,
                "errors": ser.errors
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class get_tariff(APIView):
    def post(self, request):
        ser = tariffserializers(tariff.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class get_group(APIView):
    def post(self, request):
        ser = groupserializers(group.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class get_content(APIView):
    def post(self,request):
        ser=getcontentserializers(request.data)
        if ser.is_valid():
            return Response(ser.data,status=status.HTTP_200_OK)
        else:
            return Response(ser.errors,status=status.HTTP_200_OK)


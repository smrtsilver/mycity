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


# class createcategory(APIView):
#     def post(self, request):
#         # data=request.data
#         # ser=groupserializers(data=data)
#         # if ser.is_valid():
#         #     pass
#         # else:
#         #     content={
#         #         "message" : "ورودی ها صحیح نیستند"
#         #     }
#         pass


class createcontent(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        if "group" in data.keys():
            group_id=data["group"]
        else:
            group_id=None
        # try:
        #     group.objects.get(id__exact=group_id)
        # except:
        #    content={
        #        "message":"شناسه دسته بندی اشتباه است"
        #    }
        #    return Response(content,status=status.HTTP_200_OK)
        if group_id=="1":
            ser=employmentserializers(data=data)
            if ser.is_valid():
                ser.save()
                content={
                    "message":"با موفقیت ایجاد شد",
                    "created":True
                }
                return Response(content,status=status.HTTP_200_OK)
            else:
                return Response(ser.errors,status=status.HTTP_200_OK)
        elif group_id==3:
            ser=cityprobserializers(data=data)
            if ser.is_valid():
                ser.save()
                content = {
                    "message": "با موفقیت ایجاد شد",
                    "created": True
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(ser.errors, status=status.HTTP_200_OK)
        else:
            ser = contentserializers(data=data)
            if ser.is_valid():
                ser.save()
                content = {
                    "message": "با موفقیت ایجاد شد",
                    "created": True
                }
                return Response(content, status=status.HTTP_200_OK)
            else:

                return Response(ser.errors, status=status.HTTP_201_CREATED)

class get_tariff(APIView):
    def post(self, request):
        ser = tariffserializers(tariff.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class get_group(APIView):
    def post(self, request):
        ser = groupserializers(group.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

class get_content(APIView):
    def post(self, request):
        data = request.data
        id = data["id"]
        query = content.objects.filter(group_id=id).filter(valid__exact=True).order_by("create_time")
        ser = getcontentserializers(query, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)
        # else:
        #     return Response(ser.errors,status=status.HTTP_200_OK)
        #



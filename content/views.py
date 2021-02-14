from django.contrib.auth.decorators import login_required
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
            group_id = data["group"]
        else:
            group_id = None
        # try:
        #     group.objects.get(id__exact=group_id)
        # except:
        #    content={
        #        "message":"شناسه دسته بندی اشتباه است"
        #    }
        #    return Response(content,status=status.HTTP_200_OK)
        if group_id == "1":
            ser = employmentserializers(data=data)
            if ser.is_valid():
                ser.save()
                content = {
                    "message": "با موفقیت ایجاد شد",
                    "created": True
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(ser.errors, status=status.HTTP_200_OK)
        elif group_id == 3:
            ser = cityprobserializers(data=data)
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
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        if (request.data.get("group") is None) or int(request.data["group"]) == 0:
            ser = groupserializers(group.objects.filter(parent=None), many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            group_id = request.data.get("group")
            ser = groupserializers(group.objects.filter(parent__id=group_id), many=True)
            return Response(ser.data, status=status.HTTP_200_OK)


# class get_subgroup(APIView):
#     def post(self, request):
#         data = request.data
#         if "group" in data.keys():
#             group_id = data["group"]
#
#             query = sub_group.objects.filter(category_connect__id=group_id)
#             ser = subgrouoserializers(query, many=True)
#
#             return Response(ser.data, status=status.HTTP_200_OK)
#         else:
#             data = {"group": "این فیلد لازم است"}
#             return Response(data, status=status.HTTP_200_OK)


class get_content(APIView):
    def post(self, request):
        data = request.data
        if all(x in data.keys() for x in ['group', 'skip']) and (data.get("group") != "") and (data.get("skip") != ""):
            step = 10
            skip = int(data["skip"])
            group_id = data["group"]
            query = base_content.objects.filter(group_id=group_id).order_by("create_time")[skip:skip + step]
            ser = contentserializers(query, many=True)

            # dic={
            #     "result" : ser.data,
            #     "top": top.data
            # }
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            data = {"group": "این فیلد لازم است",
                    "skip": "این فیلد لازم است"}
            return Response(data, status=status.HTTP_200_OK)

        # else:
        #     return Response(ser.errors,status=status.HTTP_200_OK)
        #


class get_slider(APIView):
    def post(self, request):
        #todo id group
        top = 3
        results = sorted(base_content.objects.all(), key=lambda m: m.number_of_likes, reverse=True)[:top]
        toplist = topcontentserializers(results, many=True)
        return Response(toplist.data, status=status.HTTP_200_OK)


@login_required
class comment_remove(APIView):
    pass

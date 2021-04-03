from sre_parse import SPECIAL_CHARS
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
# import requests
# new_token = Token.objects.create(user=request.user)
# from accounts.models import sms
# from rest_framework.views import APIView
# import pyotp
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.admin import User
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from accounts.serializers import *
# from accounts.utils import sendsmsmethod
# from django.contrib.auth.decorators import login_required
# Create your views here.
from content.serializers import *
from django.db.models import Q

from content.utils import modify_input_for_multiple_files

class get_tariff(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):



        appquery=tariffModel.objects.filter(platform__exact=1)
        Telegramquery=tariffModel.objects.filter(platform__exact=2)
        Instagramquery=tariffModel.objects.filter(platform__exact=3)
        serapp = list(tariffserializers(appquery, many=True).data)
        sertelegram = list(tariffserializers(Telegramquery, many=True).data)
        serinstagram = list(tariffserializers(Instagramquery, many=True).data)

        serapp.insert(0,{"sub" : "اپلیکیشن"})
        sertelegram.insert(0,{"sub" : "تلگرام"})
        serinstagram.insert(0,{"sub" : "اینستاگرام"})
        data={
            "APP" : serapp,
            "Telegram" : sertelegram,
            "Instagram" : serinstagram,
        }
        return Response(data,status=status.HTTP_200_OK)

class get_Special(APIView):
    def get(self,request):
        query=base_content.objects.filter(valid__exact=1).filter(Special__exact=True).orderby("-startshowtime")[:10]
        ser = getcontentserializer(query, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class delete_content(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        id = request.data.get("id")
        if id:
            user_profile = request.user.userprofile
            query = get_object_or_404(base_content, author=user_profile, id=id)
            query.delete_post()
            context = {
                "detail": "پست با موفقیت پاک شد"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "detail": "لطفا شماره ایدی پست را ارسال کنید"
            }
            return Response(context, status=status.HTTP_200_OK)


class get_group(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):

        if (request.data.get("group") is None) or int(request.data["group"]) == 0:
            ser = groupserializers(group.objects.filter(parent=None), many=True)
            a = ser.data
            a[0], a[1] = a[1], a[0]
            a[1], a[2] = a[2], a[1]
            return Response(a, status=status.HTTP_200_OK)
        else:
            group_id = request.data.get("group")
            ser = groupserializers(group.objects.filter(parent__id=group_id), many=True)
            return Response(ser.data, status=status.HTTP_200_OK)


class create_content(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FileUploadParser)

    def post(self, request):
        global arr
        data = request.data
        content = contentserializers(data=request.data, context={'request': request})
        if content.is_valid():
            obj = content.save(author=request.user.userprofile)
        else:
            return Response(content.errors, status=status.HTTP_200_OK)

        if "image" in request.data:
            images = dict((request.data).lists())['image']
            arr = []
            for number, img_name in enumerate(images):
                modified_data = modify_input_for_multiple_files(obj.get_album,
                                                                img_name)
                file_serializer = ImageSerializer(data=modified_data)
                if file_serializer.is_valid():
                    if not number:
                        file_serializer.save(mainpic=True)
                    else:
                        file_serializer.save()
                    arr.append(file_serializer.data)
                else:
                    return Response(file_serializer.errors, status=status.HTTP_200_OK)
            # ToDO add device admin
            context = {
                "created": True,
                "id": obj.id

            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            # ToDO add device admin
            context = {
                "created": True,
                "id": obj.id

            }

            return Response(context, status=status.HTTP_200_OK)

        # ser=ImageSerializer(data=data)
        # a=dict((request.data).lists())['image']
        #######
        # if request.FILES:
        #     photos = dict((request.FILES).lists()).get('image', None)
        #     if photos:
        #         for photo in photos:
        #             photo_data = {}
        #             photo_data["album"] = request.data["album"]
        #             photo_data["image"] = photo
        #             photo_serializer = ImageSerializer(data=photo_data)
        #             photo_serializer.is_valid(raise_exception=True)
        #             photo_serializer.save()
        # ser = ImageSerializer(data=data)
        # if ser.is_valid():
        #     ser.save(album=obj.get_album)
        #     return Response(ser.data)

        # ser=createcontenserializers(data=request.data)
        # ser = contentserializers(data=request.data)

        # else:
        #     return Response(ser.errors, status=status.HTTP_200_OK)
        # try:
        #     group.objects.get(id__exact=group_id)
        # except:
        #    content={
        #        "message":"شناسه دسته بندی اشتباه است"
        #    }
        #    return Response(content,status=status.HTTP_200_OK)
        # if group_id == "1":
        #     ser = employmentserializers(data=data)
        #     if ser.is_valid():
        #         ser.save()
        #         content = {
        #             "message": "با موفقیت ایجاد شد",
        #             "created": True
        #         }
        #         return Response(content, status=status.HTTP_200_OK)
        #     else:
        #         return Response(ser.errors, status=status.HTTP_200_OK)
        # elif group_id == 3:
        #     ser = cityprobserializers(data=data)
        #     if ser.is_valid():
        #         ser.save()
        #         content = {
        #             "message": "با موفقیت ایجاد شد",
        #             "created": True
        #         }
        #         return Response(content, status=status.HTTP_200_OK)
        #     else:
        #         return Response(ser.errors, status=status.HTTP_200_OK)
        # else:
        #     ser = contentserializers(data=data)
        #     if ser.is_valid():
        #         ser.save()
        #         content = {
        #             "message": "با موفقیت ایجاد شد",
        #             "created": True
        #         }
        #         return Response(content, status=status.HTTP_200_OK)
        #     else:
        #
        #         return Response(ser.errors, status=status.HTTP_201_CREATED)


class get_content(APIView):
    def post(self, request):
        data = request.data
        ser = getcontentserializer(data=data)
        if ser.is_valid():
            skip = ser.validated_data["skip"]
            city = ser.validated_data["city"]
            group_id = ser.validated_data["group"]
            search = ser.validated_data.get('search', None)
            step = 10
            city_id_list = citymodel.objects.all().values_list('id', flat=True)
            model_filter = Q()
            if search is not None:
                model_filter = Q(title__icontains=search) | Q(description__icontains=search)

            if city == 0:
                query = base_content.objects.filter(Special__exact=False).filter(group_id=group_id).filter(valid__exact=1).filter(
                    model_filter).order_by(
                    "create_time")[
                        skip:skip + step]
            elif city in city_id_list:
                query = base_content.objects.filter.filter(Special__exact=False).filter(group_id=group_id).filter(valid__exact=1).filter(
                    city_id=city).filter(
                    model_filter).order_by(
                    "create_time")[
                        skip:skip + step]
            else:
                context = {"message": "شهر با این آیدی وجود ندارد"}
                return Response(context, status=status.HTTP_200_OK)
            ser = contentserializers(query, many=True, context={"request": request})
            return Response(ser.data, status=status.HTTP_200_OK)
        # if all(x in data.keys() for x in ['city','group', 'skip','search']) and (data.get("group") != "") and (data.get("skip") != ""):
        #     try:
        #         skip = int(data["skip"])
        #         city=int(data["city"])
        #         group_id = data["group"]
        #     except:
        #         data = {"message":"مقادیر صحیح نیستند"}
        #         return Response(data,status=status.HTTP_200_OK)
        #     else:

        else:

            return Response(ser.errors, status=status.HTTP_200_OK)


class get_slider(APIView):
    def post(self, request):
        # todo id group
        group_id = request.data.get("group")
        if group_id:
            top = 5
            results = sorted(base_content.objects.filter(group__id=group_id).filter(valid__exact=1),
                             key=lambda m: m.number_of_likes, reverse=True)[:top]
            toplist = topcontentserializers(results, many=True)
            return Response(toplist.data, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "مقدار شماره گروه لازم است"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class comment_remove(APIView):
    pass


class getorset_like_bookmark(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if any(x in ["post_id", "type"] for x in request.data.keys()):
            type = request.data["type"]
            try:
                query = base_content.objects.get(id=request.data.get("post_id"))

            except:
                context = {"message": "پست یافت نشد!"}
                return Response(context, status=status.HTTP_200_OK)
            else:
                if type == "bookmark":
                    bookmarkobj = query.get_bookmark(user_id=request.user.userprofile.id)
                    if bookmarkobj.exists():
                        bookmarkobj.delete()
                        return Response({"bookmarked": False}, status=status.HTTP_200_OK)
                    else:
                        bookmark.objects.create(user_connect_id=request.user.userprofile.id, content_connect=query)
                        return Response({"bookmarked": True}, status=status.HTTP_200_OK)
                elif type == "like":
                    likeobj = query.get_like(user_id=request.user.userprofile.id)
                    if likeobj.exists():
                        likeobj.delete()
                        return Response({"liked": False}, status=status.HTTP_200_OK)
                    else:
                        like.objects.create(user_connect_id=request.user.userprofile.id, content_connect=query)
                        return Response({"liked": True}, status=status.HTTP_200_OK)
                else:
                    context = {
                        "message": "متد درستی صدا زده نشده است"
                    }
                    return Response(context, status=status.HTTP_200_OK)
        else:
            context = {"message": "آیدی پست ارسال نشده است"}
            return Response(context, status=status.HTTP_200_OK)


class getcity(APIView):
    def post(self, request):
        query = citymodel.objects.all()
        ser = cityserializers(query, many=True)
        a = list(ser.data)
        a.insert(0, {"id": 0, "city_name": "همه"})
        return Response(a, status=status.HTTP_200_OK)


class get_mycard(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_profile = request.user.userprofile
        query = base_content.objects.filter(author=user_profile).order_by("create_time")
        ser = contentserializers(query, many=True, context={"request": request})
        return Response(ser.data, status=status.HTTP_200_OK)


class get_favorite(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        query = base_content.objects.filter(post_bookmark__user_connect=user.userprofile)
        ser = contentserializers(query, many=True, context={"request": request})
        return Response(ser.data, status=status.HTTP_200_OK)

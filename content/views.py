from django.contrib.auth.decorators import login_required
from rest_framework.parsers import FileUploadParser, MultiPartParser
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
from content.utils import modify_input_for_multiple_files


class get_tariff(APIView):
    def post(self, request):
        ser = tariffserializers(tariff.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class get_group(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
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

class createcontent(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FileUploadParser)

    # parser_classes = (FileUploadParser,)
    # MultiPartParser
    def post(self, request):
        global arr
        data = request.data
        content = contentserializers(data=request.data, context={'request': request})
        if content.is_valid():
            obj = content.save(author=request.user.profile)
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
            context = {
                "message": "آگهی با موفقیت ایجاد شد و پس از تایید نمایش داده می شود",

            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "message": "آگهی با موفقیت ایجاد شد و پس از تایید نمایش داده می شود",
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
        if all(x in data.keys() for x in ['group', 'skip']) and (data.get("group") != "") and (data.get("skip") != ""):
            step = 10
            skip = int(data["skip"])
            group_id = data["group"]
            query = base_content.objects.filter(group_id=group_id).filter(valid__exact=True).order_by("create_time")[
                    skip:skip + step]
            ser = contentserializers(query, many=True, context={"request": request})
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
        # todo id group
        top = 3
        results = sorted(base_content.objects.all(), key=lambda m: m.number_of_likes, reverse=True)[:top]
        toplist = topcontentserializers(results, many=True)
        return Response(toplist.data, status=status.HTTP_200_OK)


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
                    bookmarkobj = query.get_bookmark(user_id=request.user.profile.id)
                    if bookmarkobj.exists():
                        bookmarkobj.delete()
                        return Response({"bookmarked": False}, status=status.HTTP_200_OK)
                    else:
                        bookmark.objects.create(user_connect_id=request.user.profile.id, content_connect=query)
                        return Response({"bookmarked": True}, status=status.HTTP_200_OK)
                elif type == "like":
                    likeobj = query.get_like(user_id=request.user.profile.id)
                    if likeobj.exists():
                        likeobj.delete()
                        return Response({"liked": False}, status=status.HTTP_200_OK)
                    else:
                        like.objects.create(user_connect_id=request.user.profile.id, content_connect=query)
                        return Response({"liked": True}, status=status.HTTP_200_OK)
                else:
                    context = {
                        "message": "متد درستی صدا زده نشده است"
                    }
                    return Response(context, status=status.HTTP_200_OK)
        else:
            context = {"message": "آیدی پست ارسال نشده است"}
            return Response(context, status=status.HTTP_200_OK)


# class getorsetlike(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         if "post_id" in request.data.keys():
#             try:
#                 query = base_content.objects.get(id=request.data.get("post_id"))
#
#             except:
#                 context = {"message": "پست یافت نشد!"}
#                 return Response(context, status=status.HTTP_200_OK)
#             else:
#                 likeobj = query.get_like(user_id=request.user.profile.id)
#                 if likeobj.exists():
#                     likeobj.delete()
#                     return Response({"liked": False}, status=status.HTTP_200_OK)
#                 else:
#                     like.objects.create(user_connect_id=request.user.profile.id, content_connect=query)
#                     return Response({"liked": True}, status=status.HTTP_200_OK)
#
#         else:
#             context = {"message": "آیدی پست ارسال نشده است"}
#             return Response(context, status=status.HTTP_200_OK)


class get_mycard(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_profile = request.user.profile
        query = base_content.objects.filter(author=user_profile).order_by("create_time")
        ser = contentserializers(query, many=True, context={"request": request})
        return Response(ser.data, status=status.HTTP_200_OK)

from django.contrib.auth import authenticate, login
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import sms
from accounts.serializers import *
from accounts.utils import sendsmsmethod
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
# from rest_framework.authtoken.admin import User
import pyotp
from rest_framework.authtoken.models import Token


# import requests
# new_token = Token.objects.create(user=request.user)

class anonymous(APIView):

    def post(self, request):
        global user
        # TODO set validator for number
        ser = PhoneNumberSerializer(data=request.data)
        if ser.is_valid():
            try:
                user = ser.validated_data["username"]
                usernumber = User.objects.get(username=user)
            except User.DoesNotExist:
                # age nabod
                # request to sms panel
                out = sendsmsmethod(number=user)
                if out["success"]:
                    content = {"message": "کاربر وجود ندارد",
                               "InvalidInput": False,
                               "UserExist": False,
                               "smscode": out["message"]
                               }
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    content = {
                        "message": out["message"]
                    }
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                # age bod
                content = {"message": "کاربر قبلا ثبت نام کرده است",
                           "InvalidInput": False,
                           "UserExist": True,
                           }

                return Response(content, status=status.HTTP_200_OK)
        else:
            # age vorodi dorost nbod
            content = {
                'message': ser.errors,
                "InvalidInput": True,
                "UserExist": False,

            }
            return Response(content, status=status.HTTP_200_OK)


class logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.data.get("fcm_token"):
            try:
                device = FCMDevice.objects.get(user=request.user, registration_id=request.data.get("fcm_token"))
            except FCMDevice.DoesNotExist:
                pass
            else:
                device.active = False
                device.save()
        else:
            context = {
                "detail": "پوش توکن ارسال نشده است"
            }
            return Response(context, status=status.HTTP_200_OK)


class login_user(APIView):

    def post(self, request):
        serializer = loginserializers(data=request.data)
        if serializer.is_valid():
            json = serializer.data
            try:
                user = authenticate(username=json['username'], password=json['password'])
                if user:
                    # login(request, user)
                    pushToken = json['fcm_token']
                    device = FCMDevice.objects.get_or_create(user=user, registration_id=pushToken)
                    device.type = json['type']
                    device.name = json['name']
                    device.active = True
                    device.save()
                    content = {
                        "message": "ورود موفقیت آمیز بود",
                        "authenticate": True,
                        "Token": user.auth_token.key

                    }
                    login(request, user)
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    content = {
                        "message": "نام کاربری یا رمز عبور اشتباه است",
                        "authenticate": False
                    }
                    return Response(content, status=status.HTTP_200_OK)
            except:
                content = {
                    "message": "ارور نامشخص"
                }
                return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            content = {
                "message": "ورودی ها صحیح نیست",
                "authenticate": False,
                "error": serializer.errors

            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class signup(APIView):

    def post(self, request):
        serializer = loginserializers(data=request.data)
        if serializer.is_valid():
            try:
                json = serializer.data
                user = User.objects.get(username=json['username'])
            except User.DoesNotExist:
                user = User.objects.create_user(username=json['username'], password=json['password'])
                fcm_token = json['fcm_token']
                device = FCMDevice()
                device.registration_id = fcm_token
                device.type = json['type']
                device.name = json['name']
                device.user = user
                device.active = True
                device.save()
                content = {
                    "message": "ثبت نام با موفقیت انجام شد",
                    "user_created": True,
                    "Token": user.auth_token.key
                }
                user = authenticate(username=json['username'], password=json['password'])
                login(request, user)
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                content = {
                    "message": "کاربر قبلا ثیت نام کرده است، لطفا وارد شوید"

                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)



        else:
            content = {
                "message": "ورودی ها صحیح نیست",
                "error": serializer.errors
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class forgotpass(APIView):

    def post(self, request):
        data = request.data
        ser = resetserializers(data=data)
        if ser.is_valid():
            username = ser.validated_data["username"]
            password = ser.validated_data["password"]
            smscode = ser.validated_data["smscode"]
            try:
                user = User.objects.get(username=username)
                number = sms.objects.get(phonenumber=user.username)
            except:
                # age nabod
                content = {"message": "بروز خطا در اختصاص پیامک یا یافتن کاربر",
                           }
                return Response(content, status=status.HTTP_200_OK)
            else:
                if number.authenticate(smscode):
                    user.set_password(password)
                    user.save()
                    content = {
                        "message": "پسورد با موفقیت تغییر پیدا کرد",
                        "status": True
                    }
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    content = {
                        "message": "کد اشتباه وارد شده است",
                        "status": False
                    }
                    return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(ser.errors, status=status.HTTP_200_OK)


class sendsms(APIView):

    def post(self, request, format=None):

        data = request.data
        ser = PhoneNumberSerializer(data=data)
        if ser.is_valid():
            username = ser.data["username"]
            if "method" in request.data.keys():
                if request.data.get("method") == "resetpass":
                    try:
                        user = User.objects.get(username=username)
                    except Exception as e:
                        # Todo karbar nabod chi???
                        content = {
                            "message": "کاربر یافت نشد",
                            "status": False
                        }
                        return Response(content, status=status.HTTP_200_OK)
                    else:
                        out = sendsmsmethod(number=user.username)
                        if out["success"]:
                            content = {
                                "smscode": out["message"],
                                "status": out["success"]
                            }
                            return Response(content, status=status.HTTP_200_OK)
                        else:
                            content = {
                                "status": out["success"]
                            }
                            return Response(content, status=status.HTTP_200_OK)
                elif request.data.get("method") == "sendsms":
                    out = sendsmsmethod(number=username)
                    if out["success"]:
                        content = {
                            "smscode": out["message"]
                        }
                        return Response(content, status=status.HTTP_200_OK)
                    else:
                        content = {
                            "smscode": out["success"]
                        }
                        return Response(content, status=200)
                else:
                    content = {
                        "message": "لطفا متد را ارسال کنید"
                    }
                    return Response(content, status=status.HTTP_200_OK)
            else:
                content = {
                    "message": "لطفا متد را ارسال کنید"
                }
                return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_200_OK)


class smsvalidation(APIView):

    # @permission_classes([permissions.IsAuthenticated])
    def post(self, request, format=None):

        data = request.data
        ser = smsserializers(data=data)
        if ser.is_valid():
            user = ser.validated_data["username"]
            smscode = ser.validated_data["smscode"]
            number = sms.objects.get_or_create(phonenumber=user)

            if number[0].authenticate(smscode):

                content = {
                    "authenticate": True
                }

                return Response(content, status=201)
            else:
                content = {
                    "message": "کد وارد شده نادرست است یا منقضی شده است",
                    "authenticate": False
                }

                return Response(content, status=200)


        else:

            return Response(ser.errors, status=status.HTTP_200_OK)


# class changepassword(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         serializer = loginserializers(data=request.data)
#         if serializer.is_valid():
#             username = serializer.data["username"]
#             password = serializer.data["password"]
#             try:
#                 user = User.objects.get(username=username)
#             except Exception as e:
#                 content = {
#                     "message": "کاربر یافت نشد",
#                     "errorcontent": e
#                 }
#                 return Response(content, status=status.HTTP_200_OK)
#             else:
#                 user.set_password(password)
#                 user.save()
#                 content = {
#                     "message": "پسورد با موفقیت تغییر پیدا کرد",
#                     "success": True
#                 }
#                 return Response(content, status=status.HTTP_200_OK)
#         else:
#             content = {
#                 "message": "ورودی ها معتبر نیستند",
#                 "errorcontent": serializer.errors
#             }
#             return Response(content, status=status.HTTP_400_BAD_REQUEST)

class changeprofiledetails(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def post(self, request):
        if "method" in request.data.keys():
            method = request.data.get("method")
            query = profile.objects.filter(user=request.user)
            if method == "show":
                ser = profileuserserializers(query, many=True)
                return Response(ser.data, status=status.HTTP_200_OK)
            elif method == "edit":
                serializer = profileuserserializers(query[0], data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    context = {"data": serializer.data,
                               "message": "تغییرات با موفقیت انجام شد"}
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context = {"data": serializer.errors,
                               "message": "بروز خطا"}
                    return Response(context, status=status.HTTP_200_OK)

            # ser = profileuserserializers(data=request.data, instance=query[0],partial=True)
            # if ser.is_valid():
            #     context = {"data": ser.data,
            #                "message": "تغییرات با موفقیت انجام شد"}
            # else:
            #     context = {"data": ser.errors,
            #                "message": "بروز خطا"}
            # return Response(context, status=status.HTTP_200_OK)
            else:

                context = {"message": "نام متد ارسال شده معتبر نیست"}

                return Response(context, status=status.HTTP_200_OK)

        else:
            context = {"message": "نام متد ارسال نشده"}

            return Response(context, status=status.HTTP_200_OK)

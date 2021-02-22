import pyotp
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.parsers import  MultiPartParser

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


# permission_classes = (IsAuthenticated,)
class anonymous(APIView):
    # permission_classes = (IsAuthenticated,)
    # def get(self, request):
    #     content = {'message': 'use '}
    #     return Response(content)
    def post(self, request):
        global user
        # TODO set validator for number
        print("anonymous",request.headers)
        ser = PhoneNumberSerializer(data=request.data)
        if ser.is_valid():

            # request.session['username'] = user
            # user = int(user)
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


class login_user(APIView):
    # permission_classes = (IsAuthenticated,)
    # def get(self, request):
    #     content = {
    #         "message": "invalid request, req with post method"
    #     }
    #     return Response(content)

    def post(self, request):
        serializer = loginserializers(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            password = serializer.data["password"]
        else:
            content = {
                "message": "ورودی ها صحیح نیست",
                "authenticate": False,
                "error": serializer.errors

            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            # data = request.data
            # username = data.get("username")
            # password = data.get("password")
            # if not username or not password:
            #     content = {
            #         "message": "incorrect input",
            #         "authenticate": False
            #     }
            #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if user:
                # login(request, user)
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


class signup(APIView):
    # permission_classes = (IsAuthenticated,)
    # def get(self, request):
    #     content = {
    #         "message": "invalid request, req with post method"
    #     }
    #     return Response(content)

    def post(self, request):
        serializer = loginserializers(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            password = serializer.data["password"]

        else:
            content = {
                "message": "ورودی ها صحیح نیست",
                "error": serializer.errors
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            # data = request.data
            # username = data.get("username")
            # password = data.get("password")
            # if username and password:
            user = User.objects.get(username=username)

        # else:
        #
        #     content = {
        #         "message": "invalid input"
        #     }
        #     return Response(content,status=status.HTTP_400_BAD_REQUEST)
        except:
            user = User.objects.create_user(username=username, password=password)
            content = {
                "message": "ثبت نام با موفقیت انجام شد",
                "user_created": True,
                "Token": user.auth_token.key
            }
            user = authenticate(username=username, password=password)
            login(request, user)
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {
                "message": "کاربر قبلا ثیت نام کرده است، لطفا وارد شوید"

            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


# class smsvalidation(APIView):
#
#
#     # def get(self,request):
#     #     content = {
#     #         "smsCode": smscode
#     #     }
#     #     return Response(content, status=status.HTTP_200_OK)
#
#     def post(self,request):
#
#         ser = smsserializers(data=request.data)
#         if ser.is_valid():
#             sendsms=ser.data["sendsms"]
#             user=ser.data["username"]
#             if sendsms:
#                 #todo send sms
#                 smscode = 6799
#                 content={
#                     'message' : " پیامک ارسال شد"
#                 }
#                 return Response(content,status=status.HTTP_200_OK)
#             else:
#                 sms=ser.data["smscode"]
#
#
#         sms = data.get("smscode")
#         if sms:
#             sms=int(sms)
#             if sms == smscode:
#                 content = {
#                     "message": "مورد قبول است",
#                     "authorizea": True
#
#                 }
#                 return Response(content, status=status.HTTP_200_OK)
#             else:
#                 content = {
#                     "message": "کد پیامکی اشتباه وارد شده است",
#                     "authorize" : False
#
#                 }
#                 return Response(content, status=status.HTTP_403_FORBIDDEN)
#         else:
#             content={
#                 "message": "لطفا کد را وارد کنید",
#                 "authorize" : False
#             }
#         return Response(content,status=status.HTTP_400_BAD_REQUEST)

class forgotpass(APIView):

    def post(self, request):

        serializer = loginserializers(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            password = serializer.data["password"]
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                content = {
                    "message": "کاربر یافت نشد",
                    "errorcontent": e
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                user.set_password(password)
                user.save()
                content = {
                    "message": "پسورد با موفقیت تغییر پیدا کرد",
                    "success": True
                }
                return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                "message": "ورودی ها معتبر نیستند",
                "errorcontent": serializer.errors
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # else:
    #         content = {
    #             'message': "ورودی صحیح نیست، لطفا نام کاربری را وارد کنید",
    #             "InvalidInput": True,
    #
    #         }
    #         return Response(content,status=status.HTTP_400_BAD_REQUEST)


class sendsms(APIView):

    def post(self, request, format=None):
        print("sendsms",request.headers)
        # @permission_classes([permissions.IsAuthenticated])
        # def send_sms_code(request, format=None):
        # Time based otp
        data = request.data
        data = data.get("username")

        # request.session['username'] = data
        if data:
            # data = int(data)
            out = sendsmsmethod(number=data)
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

            # try:
            #
            #     # user = User.objects.get(username=data)
            #     a = sms.objects.update_or_create(phonenumber=data)
            #     time_otp = pyotp.TOTP(a[0].key, interval=500)
            #     time_otp = time_otp.now()
            #     # Phone number must be international and start with a plus '+'
            #     # user_phone_number = request.user.phonenumber.number
            #     # client.messages.create(
            #     #     body="Your verification code is " + time_otp,
            #     #     from_=twilio_phone,
            #     #     to=user_phone_number
            #     # )
            #
            # except Exception as e:
            #     content = {
            #         "message": e
            #     }
            #     return Response(content)

        else:
            contet = {
                "message": "ورودی صجیج نیست"
            }
            return Response(contet)


class smsvalidation(APIView):

    # @permission_classes([permissions.IsAuthenticated])
    def post(self, request, format=None):
        print("smsvalid",request.headers)
        data = request.data
        ser=smsserializers(data=data)
        if ser.is_valid():
            user=ser.validated_data["username"]
            smscode=ser.validated_data["smscode"]
            number = sms.objects.get_or_create(phonenumber=user)

            if number[0].authenticate(smscode):
                # if request.user.authenticate(code):
                #     phone = request.user.phonenumber
                #     phone.verified = True
                #     phone.save()
                # phone = number
                # phone.verified = True
                # phone.save()
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

            return Response(ser.errors,status=status.HTTP_200_OK)

        # user = User.objects.get(username=user)

# Todo
class changepassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


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
                        return Response(context)
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

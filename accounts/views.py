from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated  # <-- Here

# new_token = Token.objects.create(user=request.user)
from accounts.serializers import loginserializers


class anonymous(APIView):
    # permission_classes = (IsAuthenticated,)
    # def get(self, request):
    #     content = {'message': 'use '}
    #     return Response(content)

    def post(self, request):
        global user
        data = request.data
        user = int(data.get("username"))
        # TODO set validator for number
        if user:
            try:
                # TODO set validator for number
                user = User.objects.get(username=user)
            except:
                # age nabod
                # request to sms panel
                content = {"message": "user does not exist",
                           "Invalid Input": False,
                           "User Exist": False,
                           "SMS Code": "6799"
                           }
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            else:
                # age bod
                content = {"message": "user is exist",
                           "Invalid Input": False,
                           "User Exist": True,
                           }

                return Response(content, status=status.HTTP_200_OK)
        else:
            # age vorodi dorost nbod
            content = {
                'message': "invalid input, please sent username",
                "Invalid Input": True,
                "User Exist": False,

            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class login(APIView):
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
                "message": serializer.errors,
                "authenticate": False
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
                    "message": "login succesfull",
                    "authenticate": True,
                    "Token": user.auth_token.key

                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {
                    "message": "incorrect password or username",
                    "authenticate": False
                }
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        except:
            content = {
                "message": "unknown error"
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
                "message": "register success",
                "user_created": True,
                "Token": user.auth_token.key
            }
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {
                "message": "user is exist, please login"

            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

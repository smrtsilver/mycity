from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from Log.models import VersionModel
from Log.serializers import logactionserializers, statusserializers, feedbackserializers


class Log_action(APIView):
    def post(self, request):
        ser = logactionserializers(data=request.data, context={"request": request})
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class server_status(APIView):
    def post(self, request):
        return Response(status.HTTP_200_OK)


class get_version(APIView):
    def get(self, request):
        obj = VersionModel.objects.filter(status=1).last()
        ser = statusserializers(obj)
        return Response(ser.data, status=status.HTTP_200_OK)


class set_feedback(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ser = feedbackserializers(data=request.data)
        if ser.is_valid():
            ser.save()
            context = {
                "message": "نظر شما با موفقیت ثبت شد"
            }

            return Response(context, status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from Log.serializers import logactionserializers


class Log_action(APIView):
    def post(self,request):
        ser=logactionserializers(data=request.data,context={"request":request})
        if ser.is_valid():
            ser.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
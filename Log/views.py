from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from Log.models import VersionModel
from Log.serializers import logactionserializers, statusserializers, feedbackserializers

# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional / useremail
mobile = '09123456789'  # Optional / user number
CallbackURL = 'http://localhost:8000/log/verify/' # Important: need to edit for realy server.

def send_request(request):
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


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

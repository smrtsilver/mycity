from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from content.models import tariffModel
from shop.serializers import paymentserializer, reqpaymentserializer
from rest_framework.response import Response
from rest_framework import status

###########################################################################################
# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client

from shop.utils import tozihat

MERCHANT = '06b5bac9-4311-42cd-aaef-a1fe2d5df17c'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional  request.user.username
CallbackURL = 'http://localhost:8000/shop/verify/'  # Important: need to edit for realy server.


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

            context={
                "RefID":result.RefID,
                "Status" : result.Status
            }
            return render(request,"shop/complete.html",context=context)


        elif result.Status == 101:
            # TODO REDIRECT TO PAYMENT COMPLETE

            context = {
                # "RefID": result.RefID,
                "Status": result.Status
            }
            return render(request, "shop/complete.html", context=context)

            # return HttpResponse('Transaction submitted : ' + str(result.Status))

        else:

            context = {
                # "RefID": result.RefID,
                "Status": result.Status
            }
            return render(request, "shop/complete.html", context=context)

            # return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))


    else:

        return HttpResponse('Transaction failed or canceled by user')


##########################################################################################


def pardakht(request):
    context = {
        "tariff": tariffModel.objects.all()
    }
    return render(request, "shop/shop.html", context=context)


def success(request):
    return render(request, "shop/complete.html")


def cart(request, id):
    context = {
        "tariff": get_object_or_404(tariffModel, id=id)
    }
    return render(request, "shop/cart.html", context=context)


class payment(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = request.data
        payrecipt = reqpaymentserializer(data=request.data, context={'request': request})
        if payrecipt.is_valid():

            tariff=payrecipt.validated_data["tariff"]
            Notes=payrecipt.validated_data["Notes"]
            postID=payrecipt.validated_data["postID"]
            totalpayment=payrecipt.validated_data["totalpayment"]
            profile=request.user.userprofile
            desc=(tozihat(tariff,Notes))
            #age pardakht movafaq bod


        else:
            return Response(payrecipt.errors, status=status.HTTP_400_BAD_REQUEST)

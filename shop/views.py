from django.shortcuts import render, get_object_or_404

# Create your views here.
from content.models import tariffModel


def pardakht(request):
    context={
        "tariff" : tariffModel.objects.all()
    }
    return render(request, "shop/shop.html", context=context)


def success(request):
    return render(request,"shop/complete.html")
def cart(request,id):

    context={
        "tariff" : get_object_or_404(tariffModel,id=id)
    }
    return render(request, "shop/cart.html", context=context)

from django.urls import path

from shop import views
name = 'shop'
urlpatterns = [
    path("",views.pardakht,name="shop"),
    path("card/<int:id>",views.cart,name="cart"),
    path("card/success",views.success,name="success")
]
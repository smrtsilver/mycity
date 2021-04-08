
from django.urls import path

from shop import views
name = 'shop'
urlpatterns = [
    # path("",views.pardakht,name="shop"),
    # path("card/<int:id>",views.cart,name="cart"),
    path("success/",views.success,name="success"),
    path("payment/",views.payment.as_view()),
]
#pardakht
urlpatterns += [
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
]

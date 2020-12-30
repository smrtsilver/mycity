from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts import views

urlpatterns = [
    path('anonymous/', views.anonymous.as_view()),
    path("login/",views.login.as_view()),
    path("signup/",views.signup.as_view()),
    path("smsvalidation/",views.smsvalidation.as_view()),
    path("sendsms/",views.sendsms.as_view()),
    path("resetpassword/",views.forgotpass.as_view()),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),



]

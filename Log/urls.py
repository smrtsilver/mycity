from django.urls import path

from Log import views

urlpatterns = [

    path("logaction/", views.Log_action.as_view()),
    path("serverstatus/", views.server_status.as_view()),
    path("version/", views.get_version.as_view()),
    path("feedback/",views.set_feedback.as_view()),

    #zarinpal
    path("request/", views.payment.as_view(), name='request'),
    path("verify/", views.verify, name='verify'),

]

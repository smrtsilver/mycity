from django.urls import path

from Log import views

urlpatterns = [

    path("logaction/",views.Log_action.as_view()),
    path("serverstatus/",views.server_status.as_view())

]

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from content import views

urlpatterns = [

    path("createcontent/",views.createcontent.as_view()),

    path("tariff/",views.get_tariff.as_view()),
    path("getcategory/",views.get_group.as_view()),
    path("getcontent/",views.get_content.as_view()),
    path("getslider/",views.get_slider.as_view())
    # path("subcategory/",views.get_subgroup.as_view())




]

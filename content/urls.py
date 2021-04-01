from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from content import views

urlpatterns = [


    path("deletecontent/", views.delete_content.as_view()),
    path("tariff/",views.get_tariff.as_view()),
    path("special/",views.get_Special.as_view()),
    path("getcategory/",views.get_group.as_view()),
    path("getcontent/",views.get_content.as_view()),
    path("getslider/",views.get_slider.as_view()),
    path("createcontent/", views.create_content.as_view()),
    # path("create_content/",views.create_content.as_view()),
    path("likeorbookmark/",views.getorset_like_bookmark.as_view()),
    path("mycard/",views.get_mycard.as_view()),
    path("getcity/",views.getcity.as_view()),
    path("favorite/",views.get_favorite.as_view())
    # path("subcategory/",views.get_subgroup.as_view())




]

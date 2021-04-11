"""nowshahrman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView


urlpatterns = [



# whatever urls you might have in here
# make sure the 'catch-all' url is placed last
    path("shop/", include("shop.urls"), name="shop"),
    # path('', RedirectView.as_view(pattern_name='', permanent=False)),
    path('admin/', admin.site.urls),
    path("accounts/",include("accounts.urls"),name="accounts"),
    path("contents/", include("content.urls"), name="content"),
    path("log/",include("Log.urls")),
    url(r'^nested_admin/', include('nested_admin.urls')),


# http post http://127.0.0.1:8000/api-token-auth/ username=vitor password=123
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
admin.site.site_header = "پنل مدیریت شهر من"
admin.site.site_title = "مدیریت شهر من"
admin.site.index_title = "به درگاه مدیریت {} خوش آمدید".format("'اپلیکیشن شهر من'")
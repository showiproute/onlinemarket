"""online_Market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from market import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'), 
    url(r'^LocationCate/(?P<locate_cateid>\d+)/$',views.LocationCate,name='LocationCate'),
    url(r'^BrandCate/(?P<brand_cateid>\d+)/$',views.BrandsCate,name='BrandCate'), 
    url(r'^BrandDetail/(?P<detail_id>\d+)/$',views.BrandDetail,name='BrandDetail'),
    url(r'^viewHistory/$',views.viewHistory,name='viewHistory'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}, name='media'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}, name='static'),   
    url(r'^check_code',views.check_code,name='check_code'),
    url(r'^about',views.about,name='about'),
    url(r'^users/',include('market.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
]


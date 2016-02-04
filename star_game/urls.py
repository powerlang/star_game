"""star_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
import django
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

from game import views

urlpatterns = [
    url(r'^$', lambda x: HttpResponseRedirect('/admin/')),
    url(r'^admin/', admin.site.urls),
    url(r'^game/', include('game.urls')),
    url(r'^media/(?P<path>.*)$', "django.views.static.serve",
        {'document_root': django.conf.settings.MEDIA_ROOT}),
]

admin.site.site_header = '路书明星游戏 管理'

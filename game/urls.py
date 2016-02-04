from django.conf.urls import patterns, url 
from .views import start_game, query_star, query_qr

urlpatterns = patterns('',
                       url(r'^$', start_game),
                       url(r'^query_star$', query_star),
                       url(r'^qr$', query_qr),
)

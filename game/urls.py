from django.conf.urls import patterns, url 
from .views import query_star

urlpatterns = patterns('',
                       url(r'^query_star$', query_star),
)

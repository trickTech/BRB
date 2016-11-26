from django.conf.urls import url
from board import views

urlpatterns = [
    url(r'^events/$', views.event_list),
    url(r'^events/(?P<pk>[0-9]+)/$', views.event_detail),
    url(r'^events/(?P<pk>[0-9]+)/vote/$', views.vote)
]

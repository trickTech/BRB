from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^user/$', views.UserList.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^auth/islogin$', views.is_login),
    url(r'^auth/auth$', views.auth_handler),
]

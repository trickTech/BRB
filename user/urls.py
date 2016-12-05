from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^auth/islogin$', views.is_login),
    url(r'^auth/auth$', views.auth_handler),
    url(r'^auth/debug$', views.debug)
]

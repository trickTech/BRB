from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^auth/callback$', views.callback_handler),
]

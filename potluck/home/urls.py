from django.urls import path

from potluck.home.views import home

urlpatterns = [path("", home)]

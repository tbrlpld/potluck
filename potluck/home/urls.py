from django.urls import path

from potluck.home.views import home

app_name = "home"

urlpatterns = [path("", home, name="home")]

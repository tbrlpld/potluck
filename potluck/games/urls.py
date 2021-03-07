from django.urls import path

from potluck.games import views

app_name = "games"

urlpatterns = [path("create/", views.CreateGameView.as_view(), name="create")]

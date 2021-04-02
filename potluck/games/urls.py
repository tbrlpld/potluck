from django.urls import path

from potluck.games import views

app_name = "games"

urlpatterns = [
    # path("", views.GameListView.as_view(), name="list"),
    path("<int:pk>/delete/", views.GameDeleteView.as_view(), name="delete"),
]

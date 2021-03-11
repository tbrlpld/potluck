from django.urls import path


from potluck.pots.views import PotListView, PotCreateView, PotDetailView, GameAddView

app_name = "pots"

urlpatterns = [
    path("", PotListView.as_view(), name="list"),
    path("<int:pk>/", PotDetailView.as_view(), name="detail"),
    path("<int:pot_id>/add-game", GameAddView.as_view(), name="add_game"),
    path("create/", PotCreateView.as_view(), name="create"),
]

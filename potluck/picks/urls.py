from django import urls

from potluck.picks.views import CreatePickView, AddGamePicksView


app_name = "picks"

urlpatterns = [
    urls.path("pot/<int:pot_id>/create/", CreatePickView.as_view(), name="create"),
    urls.path(
        "pot/<int:pot_id>/pick-games/<int:pick_id>",
        AddGamePicksView.as_view(),
        name="pick_games",
    ),
]

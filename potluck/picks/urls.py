from django import urls

from potluck.picks.views import CreatePickView, AddGamePicksView


app_name = "picks"

urlpatterns = [
    urls.path("create/", CreatePickView.as_view(), name="create"),
    urls.path("pick-games/", AddGamePicksView.as_view(), name="pick_games"),
]

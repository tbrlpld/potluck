from django import urls

from potluck.picks.views import CreateGamePickView, CreatePickView


app_name = "picks"

urlpatterns = [
    urls.path("pick/", CreatePickView.as_view(), name="pick"),
    urls.path("create/<int:game_id>/", CreateGamePickView.as_view(), name="create"),
]

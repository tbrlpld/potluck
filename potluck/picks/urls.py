from django import urls

from potluck.picks.views import CreateGamePickView


app_name = "picks"

urlpatterns = [
    urls.path("create/<int:game_id>/", CreateGamePickView.as_view(), name="create")
]

"""potluck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from potluck.games.views import GameDeleteView
from potluck.picks.views import pick_create_view
from potluck.pots.views import (
    AddGameView,
    PotCreateView,
    PotDetailView,
    PotListView,
    SetWinningTeamsView,
    TallyView,
    UpdatePotStatusView,
)


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("djng/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    # path("", include("potluck.home.urls", name§space="home")),
    #
    path("", PotListView.as_view(), name="pots_list"),
    path("pots/create/", PotCreateView.as_view(), name="pot_create"),
    path("pots/<int:pk>/", PotDetailView.as_view(), name="pot_detail"),
    path(
        "pots/<int:pk>/update-status/",
        UpdatePotStatusView.as_view(),
        name="pot_update_status",
    ),
    path("pots/<int:pot_id>/add-game/", AddGameView.as_view(), name="add_game"),
    path(
        "pots/<int:pot_id>/winners/", SetWinningTeamsView.as_view(), name="set_winners"
    ),
    path(
        "pots/<int:pot_id>/place-pick/",
        pick_create_view,
        name="pick_create",
    ),
    path(
        "pots/<int:pot_id>/tally/",
        TallyView.as_view(),
        name="show_tally",
    ),
    #
    path(
        "games/<int:pk>/delete/",
        GameDeleteView.as_view(),
        name="game_delete",
    ),
    #
    path("sentry-debug", trigger_error),
]

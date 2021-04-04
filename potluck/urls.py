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
from django.urls import path, include

from potluck.games.views import GameDeleteView
from potluck.picks.views import CreatePickView, AddGamePicksView
from potluck.pots.views import PotListView, PotCreateView, PotDetailView, PotAddGameView


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    # path("", include("potluck.home.urls", name§space="home")),
    #
    path("", PotListView.as_view(), name="pots_list"),
    path("pots/create/", PotCreateView.as_view(), name="pot_create"),
    path("pots/<int:pk>/", PotDetailView.as_view(), name="pot_detail"),
    path("pots/<int:pot_id>/add-game", PotAddGameView.as_view(), name="game_add"),
    path(
        "pots/<int:pot_id>/picks/create", CreatePickView.as_view(), name="pick_create"
    ),
    path(
        "pots/<int:pot_id>/picks/<int:pick_id>/pick-games",
        AddGamePicksView.as_view(),
        name="games_pick",
    ),
    #
    path("games/<int:pk>/delete/", GameDeleteView.as_view(), name="game_delete"),
    #
]

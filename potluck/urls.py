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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

from potluck.games import views as games_views
from potluck.picks import views as picks_views
from potluck.pots import views as pots_views

urlpatterns = [
    path("dj-admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    # path("", include("potluck.home.urls", namespace="home")),
    #
    path("", pots_views.PotList.as_view(), name="pots_list"),
    path("pots/create/", pots_views.PotCreate.as_view(), name="pot_create"),
    path("pots/<int:pk>/", pots_views.PotDetail.as_view(), name="pot_detail"),
    path("pots/<int:pk>/delete", pots_views.PotDelete.as_view(), name="pot_delete"),
    path(
        "pots/<int:pk>/update-status/",
        pots_views.UpdatePotStatus.as_view(),
        name="pot_update_status",
    ),
    path(
        "pots/<int:pot_id>/add-game/", games_views.CreateGame.as_view(), name="add_game"
    ),
    path(
        "pots/<int:pot_id>/set-results/",
        games_views.set_results,
        name="set_results",
    ),
    path(
        "pots/<int:pot_id>/submit-pick-sheet/",
        picks_views.submit_pick_sheet,
        name="submit_pick_sheet",
    ),
    path(
        "pots/<int:pot_id>/tally/",
        picks_views.Tally.as_view(),
        name="show_tally",
    ),
    #
    path(
        "games/<int:pk>/delete/",
        games_views.DeleteGame.as_view(),
        name="game_delete",
    ),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

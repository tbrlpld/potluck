import http

from django import test, urls

import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.models import GamePick, Pick
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPickCreateView:
    def test_get_success(self):
        pot = PotFactory.create()
        url = urls.reverse("pick_create", kwargs={"pot_id": pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_get_display_game_titles(self):
        pot = PotFactory.create()
        game_1 = pot.games.first()
        game_2 = pot.games.last()
        url = urls.reverse("pick_create", kwargs={"pot_id": pot.id})
        client = test.Client()

        response = client.get(url)

        assert str(game_1) in str(response.content)
        assert str(game_2) in str(response.content)

    def test_post_creates_pick_and_game_picks(self):
        pot = PotFactory.create()
        game_1 = pot.games.first()
        game_2 = pot.games.last()
        picked_team_1 = game_1.teams.first()
        picked_team_2 = game_2.teams.first()
        picker_name = "Test Picker"
        data = {
            "pot": pot.id,
            "picker": picker_name,
            "form-INITIAL_FORMS": 2,
            "form-TOTAL_FORMS": 2,
            "form-MAX_NUM_FORMS": 2,
            "form-MIN_NUM_FORMS": 2,
            "form-0-game": game_1.id,
            "form-0-picked_team": picked_team_1.id,
            "form-1-game": game_2.id,
            "form-1-picked_team": picked_team_2.id,
        }
        url = urls.reverse("pick_create", kwargs={"pot_id": pot.id})
        client = test.Client()

        response = client.post(url, data=data, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        assert Pick.objects.count() == 1
        assert GamePick.objects.count() == 2
        pick = Pick.objects.first()
        assert pick.game_picks.first().picked_team == picked_team_1
        assert pick.game_picks.last().picked_team == picked_team_2

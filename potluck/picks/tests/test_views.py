import http

from django import test
from django import urls
import pytest

from potluck.pots.tests.factories import PotFactory
from potluck.games.tests.factories import GameFactory


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
        game_1 = GameFactory.create_with_teams(pot=pot)
        game_2 = GameFactory.create_with_teams(pot=pot)
        url = urls.reverse("pick_create", kwargs={"pot_id": pot.id})
        client = test.Client()

        response = client.get(url)

        assert str(game_1) in str(response.content)
        assert str(game_2) in str(response.content)

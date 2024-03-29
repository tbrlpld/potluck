import http

from django import test, urls

import pytest

from potluck.games import factories as games_factories
from potluck.games import models as games_models
from potluck.pots.tests import factories as pots_factories


@pytest.mark.django_db
class TestCreateGame:
    def test_get(self):
        pot = pots_factories.PotFactory.create()
        url = urls.reverse("add_game", kwargs={"pot_id": pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK


@pytest.mark.django_db
class TestDeleteGame:
    def test_post_deletes_game(self):
        pot = pots_factories.PotFactory.create()
        game = games_factories.Game(pot=pot)
        url = urls.reverse("game_delete", kwargs={"pk": game.id})
        client = test.Client()
        assert game in games_models.Game.objects.all()

        response = client.post(url, data={}, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        assert game not in games_models.Game.objects.all()


@pytest.mark.django_db
class TestSetResults:
    @pytest.fixture
    def setup(self):
        self.pot = pots_factories.PotFactory.create()
        self.game_1 = games_factories.Game(pot=self.pot, with_teams=True)
        self.team_1 = self.game_1.away_team
        self.team_2 = self.game_1.home_team
        self.game_2 = games_factories.Game(pot=self.pot, with_teams=True)
        self.team_3 = self.game_2.away_team
        self.team_4 = self.game_2.home_team
        self.url = urls.reverse("set_results", kwargs={"pot_id": self.pot.id})
        self.client = test.Client()
        assert self.pot.games.count() == 2

    def test_get_success(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK
        assert self.team_1.name in str(response.content)
        assert self.team_2.name in str(response.content)
        assert self.team_3.name in str(response.content)
        assert self.team_4.name in str(response.content)

from http import HTTPStatus

from django import test, urls

import pytest

from potluck.games import models as games_models
from potluck.games.tests import factories as games_factories
from potluck.pots.tests import factories as pots_factories


@pytest.mark.django_db
class TestDeleteGame:
    def test_post_deletes_game(self):
        pot = pots_factories.PotFactory.create()
        game = games_factories.GameFactory.create(pot=pot)
        url = urls.reverse("game_delete", kwargs={"pk": game.id})
        client = test.Client()
        assert game in games_models.Game.objects.all()

        response = client.post(url, data={}, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert game not in games_models.Game.objects.all()

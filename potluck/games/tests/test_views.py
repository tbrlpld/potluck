from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestDeleteGame:
    def test_post_deletes_game(self):
        pot = PotFactory.create()
        game = GameFactory.create(pot=pot)
        url = reverse("game_delete", kwargs={"pk": game.id})
        client = Client()
        assert game in Game.objects.all()

        response = client.post(url, data={}, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert game not in Game.objects.all()

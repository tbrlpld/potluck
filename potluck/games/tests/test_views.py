from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory


@pytest.mark.django_db
class TestGameDeleteView:
    def test_post_deletes_game(self):
        game = GameFactory.create_with_teams()
        url = reverse("game_delete", kwargs={"pk": game.id})
        client = Client()
        assert Game.objects.count() == 1

        response = client.post(url, data={}, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert Game.objects.count() == 0

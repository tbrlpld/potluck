from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestGameAddView:
    def test_get_success(self):
        pot = PotFactory.create()
        url = reverse("game_add", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_pot_in_context(self):
        pot = PotFactory.create()
        url = reverse("game_add", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert pot == response.context["pot"]


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

from http import HTTPStatus
from django.urls import reverse
from django.test import Client
import pytest

from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestGameAddView:
    def test_success_resonse(self):
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

from http import HTTPStatus
from django.urls import reverse
from django.test import Client
import pytest

from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPotDetailView:
    def test_pot_name_in_detail_view(self):
        pot = PotFactory.create()
        url = reverse("pots:detail", kwargs={"pk": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestAddGameView:
    def test_pot_in_context(self):
        pot = PotFactory.create()
        url = reverse("pots:add_game", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert pot == response.context["pot"]
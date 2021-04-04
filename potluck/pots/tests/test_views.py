from http import HTTPStatus
from django.urls import reverse
from django.test import Client
import pytest

from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPotListView:
    def test_pot_list_empty(self):
        url = reverse("pots_list")
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_pot_list_contains_existing_pot(self):
        pot = PotFactory.create()
        url = reverse("pots_list")
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestPotDetailView:
    def test_pot_name_in_detail_view(self):
        pot = PotFactory.create()
        url = reverse("pot_detail", kwargs={"pk": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestAddGameView:
    def test_pot_in_context(self):
        pot = PotFactory.create()
        url = reverse("game_add", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert pot == response.context["pot"]

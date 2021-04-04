from http import HTTPStatus
from django.urls import reverse
from django.test import Client
import pytest

from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPotListView:
    def test_pot_list_empty(self):
        url = reverse("pots_list")
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_pot_list_contains_existing_pot_name(self):
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
class TestPotCreateView:
    def test_get_sucess(self):
        url = reverse("pot_create")
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_post_creates_pot(self):
        url = reverse("pot_create")
        client = Client()
        data = {"name": "Test Pot"}

        response = client.post(url, data=data, follow=True)

        assert response.status_code == HTTPStatus.OK
        assert Pot.objects.first().name == "Test Pot"

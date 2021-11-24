import http

from django.test import Client
from django.urls import reverse

import pytest

from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPotList:
    def test_get_success(self):
        url = reverse("pots_list")
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_pot_list_contains_existing_pot_name(self):
        pot = PotFactory.create()
        url = reverse("pots_list")
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestPotDetail:
    def test_get_success(self):
        pot = PotFactory.create()
        url = reverse("pot_detail", kwargs={"pk": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert pot.name in str(response.content)

    def test_pot_name_shown(self):
        pot = PotFactory.create()
        url = reverse("pot_detail", kwargs={"pk": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestPotCreate:
    def test_get_sucess(self):
        url = reverse("pot_create")
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_post_creates_pot(self):
        url = reverse("pot_create")
        client = Client()
        data = {"name": "Test Pot", "tiebreaker_description": "Tiebreker description"}

        response = client.post(url, data=data, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        assert Pot.objects.first().name == "Test Pot"


@pytest.mark.django_db
class TestPotDelete:
    def test_get(self):
        pot = PotFactory()
        url = reverse("pot_delete", kwargs={"pk": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_post(self):
        pot = PotFactory()
        url = reverse("pot_delete", kwargs={"pk": pot.id})
        client = Client()
        assert pot in Pot.objects.all()

        response = client.post(url, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        assert pot not in Pot.objects.all()


@pytest.mark.django_db
class TestGameAddView:
    def test_get_success(self):
        pot = PotFactory.create()
        url = reverse("add_game", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_pot_in_context(self):
        pot = PotFactory.create()
        url = reverse("add_game", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert pot == response.context["pot"]

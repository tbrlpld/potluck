import http

from django import test, urls

import pytest

from potluck.pots import models as pots_models
from potluck.pots.tests import factories as pots_factories


@pytest.mark.django_db
class TestPotList:
    def test_get_success(self):
        url = urls.reverse("pots_list")
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_pot_list_contains_existing_pot_name(self):
        pot = pots_factories.PotFactory.create()
        url = urls.reverse("pots_list")
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestPotDetail:
    def test_get_success(self):
        pot = pots_factories.PotFactory.create()
        url = urls.reverse("pot_detail", kwargs={"pk": pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert pot.name in str(response.content)

    def test_pot_name_shown(self):
        pot = pots_factories.PotFactory.create()
        url = urls.reverse("pot_detail", kwargs={"pk": pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert pot.name in str(response.content)


@pytest.mark.django_db
class TestPotCreate:
    def test_get_sucess(self):
        url = urls.reverse("pot_create")
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_post_creates_pot(self):
        url = urls.reverse("pot_create")
        client = test.Client()
        data = {"name": "Test Pot", "tiebreaker_description": "Tiebreker description"}

        response = client.post(url, data=data, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        assert pots_models.Pot.objects.first().name == "Test Pot"


@pytest.mark.django_db
class TestPotDelete:
    def test_get(self):
        pot = pots_factories.PotFactory()
        url = urls.reverse("pot_delete", kwargs={"pk": pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK

    def test_post(self):
        pot = pots_factories.PotFactory()
        url = urls.reverse("pot_delete", kwargs={"pk": pot.id})
        client = test.Client()
        assert pot in pots_models.Pot.objects.all()

        response = client.post(url, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        assert pot not in pots_models.Pot.objects.all()


@pytest.mark.django_db
class TestUpdatePotStatus:
    def test_post(self):
        pot = pots_factories.PotFactory()
        url = urls.reverse("pot_update_status", kwargs={"pk": pot.id})
        client = test.Client()
        assert pot.status == pots_models.Pot.Status.DRAFT

        response = client.post(
            url,
            data={"status": pots_models.Pot.Status.OPEN},
            follow=True,
        )

        assert response.status_code == http.HTTPStatus.OK

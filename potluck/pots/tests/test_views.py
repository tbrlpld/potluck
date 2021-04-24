from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest

from potluck.games.tests.factories import GameFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPotListView:
    def test_get_success(self):
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
    def test_get_success(self):
        pot = PotFactory.create()
        url = reverse("pot_detail", kwargs={"pk": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK
        assert pot.name in str(response.content)

    def test_pot_name_shown(self):
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


@pytest.mark.django_db
class TestGameAddView:
    def test_get_success(self):
        pot = PotFactory.create()
        url = reverse("add_game", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_pot_in_context(self):
        pot = PotFactory.create()
        url = reverse("add_game", kwargs={"pot_id": pot.id})
        client = Client()

        response = client.get(url)

        assert pot == response.context["pot"]


@pytest.mark.django_db
class TestSetWinningTeamsView:

    @pytest.fixture
    def setup(self):
        self.pot = PotFactory.create()
        self.game1 = self.pot.games.first()
        self.game2 = self.pot.games.last()
        self.url = reverse("add_game", kwargs={"pot_id": self.pot.id})
        self.client = Client()
        assert self.pot.games.count() == 2

    def test_get_success(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK

    def test_get_team_names(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        for team in self.game1.teams.all():
            assert team.name in str(response.content)
        for team in self.game2.teams.all():
            assert team.name in str(response.content)

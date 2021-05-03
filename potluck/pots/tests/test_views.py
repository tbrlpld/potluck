from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest

from potluck.picks.tests.factories import GamePickFactory, PickFactory
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


@pytest.mark.django_db
class TestTallyView:

    @pytest.fixture
    def setup(self):
        pot = PotFactory.create()

        game_1 = pot.games.first()
        game_1_winning_team = game_1.teams.first()
        game_1_loosing_team = game_1.teams.last()
        game_1.set_winning_team(game_1_winning_team)

        game_2 = pot.games.first()
        game_2_winning_team = game_2.teams.first()
        game_2_loosing_team = game_2.teams.last()
        game_2.set_winning_team(game_2_winning_team)

        # Pick 1 with 1 correct game pick
        self.pick_1 = PickFactory(pot=pot)
        GamePickFactory(
            pick=self.pick_1, game=game_1, picked_team=game_1_winning_team
        )
        GamePickFactory(
            pick=self.pick_1, game=game_2, picked_team=game_2_loosing_team
        )

        # Pick 2 with 2 correct game picks
        self.pick_2 = PickFactory(pot=pot)
        GamePickFactory(
            pick=self.pick_2, game=game_1, picked_team=game_1_winning_team
        )
        GamePickFactory(
            pick=self.pick_2, game=game_2, picked_team=game_2_winning_team
        )

        self.url = reverse("show_tally", kwargs={"pot_id": pot.id})
        self.client = Client()

    def test_get_success(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK

    def test_get_shows_picker_names(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        response_content = str(response.content)
        assert self.pick_1.picker in response_content
        assert self.pick_2.picker in response_content

    def test_get_shows_picker_names_in_order_of_correct_picks(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        response_content = str(response.content)
        picker_1_index = response_content.index(self.pick_1.picker)
        picker_2_index = response_content.index(self.pick_2.picker)
        assert picker_2_index < picker_1_index

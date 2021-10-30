from http import HTTPStatus

from django.test import Client
from django.urls import reverse

import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.tests.factories import PickFactory, PickSheetFactory
from potluck.pots.models import Pot
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


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
        self.team_1 = TeamFactory.create()
        self.team_2 = TeamFactory.create()
        self.team_3 = TeamFactory.create()
        self.team_4 = TeamFactory.create()
        self.pot = PotFactory.create()
        self.game1 = GameFactory.create(pot=self.pot)
        self.game1.teams.set((self.team_1, self.team_2))
        self.game2 = GameFactory.create(pot=self.pot)
        self.game2.teams.set((self.team_3, self.team_4))
        self.url = reverse("add_game", kwargs={"pot_id": self.pot.id})
        self.client = Client()
        assert self.pot.games.count() == 2

    def test_get_success(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK

    def test_get_team_names(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assert self.team_1.name in str(response.content)
        assert self.team_2.name in str(response.content)
        assert self.team_3.name in str(response.content)
        assert self.team_4.name in str(response.content)


@pytest.mark.django_db
class TestTallyView:
    @pytest.fixture
    def setup(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        team_3 = TeamFactory.create()
        team_4 = TeamFactory.create()
        pot = PotFactory.create()
        game_1 = GameFactory.create(pot=pot)
        game_1.teams.set((team_1, team_2))
        game_2 = GameFactory.create(pot=pot)
        game_2.teams.set((team_3, team_4))

        game_1_winning_team = team_1
        game_1.set_winning_team(game_1_winning_team)

        game_2_winning_team = team_3
        game_2_loosing_team = team_4
        game_2.set_winning_team(game_2_winning_team)

        # Pick 1 with 1 correct game pick
        self.pick_sheet_1 = PickSheetFactory(pot=pot)
        PickFactory(
            pick_sheet=self.pick_sheet_1, game=game_1, picked_team=game_1_winning_team
        )
        PickFactory(
            pick_sheet=self.pick_sheet_1, game=game_2, picked_team=game_2_loosing_team
        )

        # Pick 2 with 2 correct game picks
        self.pick_sheet_2 = PickSheetFactory(pot=pot)
        PickFactory(
            pick_sheet=self.pick_sheet_2, game=game_1, picked_team=game_1_winning_team
        )
        PickFactory(
            pick_sheet=self.pick_sheet_2, game=game_2, picked_team=game_2_winning_team
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
        assert self.pick_sheet_1.picker in response_content
        assert self.pick_sheet_2.picker in response_content

    def test_get_shows_picker_names_in_order_of_correct_picks(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        response_content = str(response.content)
        picker_1_index = response_content.index(self.pick_sheet_1.picker)
        picker_2_index = response_content.index(self.pick_sheet_2.picker)
        assert picker_2_index < picker_1_index

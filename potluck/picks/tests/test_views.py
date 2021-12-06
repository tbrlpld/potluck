import http

from django import test, urls

import pytest

from potluck.games import factories as games_factories
from potluck.picks import models as picks_models
from potluck.picks.tests import factories as picks_factories
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestTally:
    @pytest.fixture
    def setup(self):
        pot = pots_factories.PotFactory.create()
        game_1 = games_factories.Game.create(pot=pot, with_teams=True)
        game_2 = games_factories.Game.create(pot=pot, with_teams=True)

        game_1_winning_team = game_1.away_team
        game_1.set_and_save_winning_team(game_1_winning_team)

        game_2_winning_team = game_2.home_team
        game_2_loosing_team = game_2.away_team
        game_2.set_and_save_winning_team(game_2_winning_team)

        # Pick 1 with 1 correct game pick
        self.pick_sheet_1 = picks_factories.PickSheetFactory(pot=pot)
        picks_factories.PickFactory(
            pick_sheet=self.pick_sheet_1, game=game_1, picked_team=game_1_winning_team
        )
        picks_factories.PickFactory(
            pick_sheet=self.pick_sheet_1, game=game_2, picked_team=game_2_loosing_team
        )

        # Pick 2 with 2 correct game picks
        self.pick_sheet_2 = picks_factories.PickSheetFactory(pot=pot)
        picks_factories.PickFactory(
            pick_sheet=self.pick_sheet_2, game=game_1, picked_team=game_1_winning_team
        )
        picks_factories.PickFactory(
            pick_sheet=self.pick_sheet_2, game=game_2, picked_team=game_2_winning_team
        )

        self.url = urls.reverse("show_tally", kwargs={"pot_id": pot.id})
        self.client = test.Client()

    def test_get_success(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK

    def test_get_shows_picker_names(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK
        response_content = str(response.content)
        assert self.pick_sheet_1.picker in response_content
        assert self.pick_sheet_2.picker in response_content

    def test_get_shows_picker_names_in_order_of_correct_picks(self, setup):
        response = self.client.get(self.url)

        assert response.status_code == http.HTTPStatus.OK
        response_content = str(response.content)
        picker_1_index = response_content.index(self.pick_sheet_1.picker)
        picker_2_index = response_content.index(self.pick_sheet_2.picker)
        assert picker_2_index < picker_1_index


@pytest.mark.django_db
class TestSubmitPickSheet:
    @pytest.fixture
    def setup_pot_with_two_games(self):
        self.pot = pots_factories.PotFactory.create()
        self.game_1 = games_factories.Game.create(pot=self.pot, with_teams=True)
        self.team_1 = self.game_1.away_team
        self.team_2 = self.game_1.home_team
        self.game_2 = games_factories.Game.create(pot=self.pot, with_teams=True)
        self.team_3 = self.game_2.home_team
        self.team_4 = self.game_2.away_team

    def test_get_success(self, setup_pot_with_two_games):
        self.team_5 = teams_factories.TeamFactory.create()
        url = urls.reverse("submit_pick_sheet", kwargs={"pot_id": self.pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
        assert self.team_1.name in str(response.content)
        assert self.team_2.name in str(response.content)
        assert self.team_3.name in str(response.content)
        assert self.team_4.name in str(response.content)
        assert self.team_5.name not in str(response.content)

    def test_post_creates_pick_and_game_picks(self, setup_pot_with_two_games):
        picked_team_1 = self.team_1
        picked_team_2 = self.team_3
        picker_name = "Test Picker"
        data = {
            "pot": self.pot.id,
            "picker": picker_name,
            "tiebreaker_guess": 0,
            "form-INITIAL_FORMS": 2,
            "form-TOTAL_FORMS": 2,
            "form-MAX_NUM_FORMS": 2,
            "form-MIN_NUM_FORMS": 2,
            "form-0-game": self.game_1.id,
            "form-0-picked_team": picked_team_1.id,
            "form-1-game": self.game_2.id,
            "form-1-picked_team": picked_team_2.id,
        }
        url = urls.reverse("submit_pick_sheet", kwargs={"pot_id": self.pot.id})
        client = test.Client()

        response = client.post(url, data=data, follow=True)

        assert response.status_code == http.HTTPStatus.OK
        pick_sheet = picks_models.PickSheet.objects.filter(pot=self.pot).first()
        assert pick_sheet.picks.count() == 2
        assert pick_sheet.picks.first().picked_team == picked_team_1
        assert pick_sheet.picks.last().picked_team == picked_team_2

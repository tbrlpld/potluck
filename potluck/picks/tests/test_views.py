import http

from django import test, urls

import pytest

from potluck.games.tests.factories import GameFactory
from potluck.picks.models import PickSheet
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestSubmitPickSheet:
    @pytest.fixture
    def setup_pot_with_two_games(self):
        self.team_1 = TeamFactory.create()
        self.team_2 = TeamFactory.create()
        self.team_3 = TeamFactory.create()
        self.team_4 = TeamFactory.create()
        self.pot = PotFactory.create()
        self.game_1 = GameFactory.create(pot=self.pot)
        self.game_1.teams.set((self.team_1, self.team_2))
        self.game_2 = GameFactory.create(pot=self.pot)
        self.game_2.teams.set((self.team_3, self.team_4))

    def test_get_success(self, setup_pot_with_two_games):
        self.team_5 = TeamFactory.create()
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
        picked_team_1 = self.game_1.teams.first()
        picked_team_2 = self.game_2.teams.first()
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
        pick_sheet = PickSheet.objects.filter(pot=self.pot).first()
        assert pick_sheet.picks.count() == 2
        assert pick_sheet.picks.first().picked_team == picked_team_1
        assert pick_sheet.picks.last().picked_team == picked_team_2

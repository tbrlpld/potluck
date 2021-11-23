import pytest

from potluck.games.tests import factories as games_factories
from potluck.picks import forms as picks_forms
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


class TestCreatePickSheet:
    def test_create_empty(self):
        with pytest.raises(TypeError):
            picks_forms.CreatePickSheet()

    def test_create_without_data(self):
        pot = pots_factories.PotFactory.build()
        form = picks_forms.CreatePickSheet(pot=pot)

        assert form.is_valid() is False

    def test_create_valid_form(self):
        pot = pots_factories.PotFactory.build()
        form = picks_forms.CreatePickSheet(
            data={
                "picker": "Joe Shmoe",
                "tiebreaker_guess": 10,
            },
            pot=pot,
        )

        assert form.is_valid() is True
        pick_sheet = form.save(commit=False)
        assert pick_sheet.pot == pot


@pytest.mark.django_db
class TestCreatePick:
    @pytest.fixture
    def setup(self):
        self.team_1 = teams_factories.TeamFactory.create()
        self.team_2 = teams_factories.TeamFactory.create()
        self.game = games_factories.GameFactory.create()
        self.game.teams.set((self.team_1, self.team_2))

    def test_empty(self):
        with pytest.raises(TypeError):
            picks_forms.CreatePick()

    def test_with_game(self, setup):
        form = picks_forms.CreatePick(game=self.game)

        assert form.is_valid() is False

    def test_with_data(self, setup):
        form = picks_forms.CreatePick(data={"picked_team": self.team_1}, game=self.game)

        assert form.is_valid() is True
        pick = form.save()
        assert pick.game == self.game
        assert pick.picked_team == self.team_1

    def test_with_team_not_from_game(self, setup):
        team_3 = teams_factories.TeamFactory.create()
        form = picks_forms.CreatePick(
            data={"picked_team": team_3},
            game=self.game,
        )

        assert form.is_valid() is False
        assert "picked_team" in form.errors

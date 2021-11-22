import pytest

from potluck.picks import forms
from potluck.games.tests import factories as games_factories
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


class TestCreatePickSheet:
    def test_create_empty(self):
        with pytest.raises(TypeError):
            forms.CreatePickSheet()

    def test_create_without_data(self):
        pot = pots_factories.PotFactory.build()
        form = forms.CreatePickSheet(pot=pot)

        assert form.is_valid() is False

    def test_create_valid_form(self):
        pot = pots_factories.PotFactory.build()
        form = forms.CreatePickSheet(
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
        with pytest.raises(ValueError):
            form = forms.CreatePick()

    def test_with_game(self, setup):
        form = forms.CreatePick(initial={"game": self.game})

        assert form.is_valid() is False

    def test_with_data(self, setup):
        form = forms.CreatePick(
            data={
                "game": self.game,
                "picked_team": self.team_1,
            },
            initial={"game": self.game},
        )

        assert form.is_valid() is True
        pick = form.save(commit=False)
        assert pick.game == self.game
        assert pick.picked_team == self.team_1

    def test_with_team_not_from_game(self, setup):
        team_3 = teams_factories.TeamFactory.create()
        form = forms.CreatePick(
            data={
                "game": self.game,
                "picked_team": team_3,
            },
            initial={"game": self.game},
        )

        assert form.is_valid() is False
        assert "picked_team" in form.errors

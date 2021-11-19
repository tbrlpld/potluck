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
    def test_create_empty(self):
        with pytest.raises(ValueError):
            form = forms.CreatePick()

    def test_with_initial(self):
        team_1 = teams_factories.TeamFactory.create()
        team_2 = teams_factories.TeamFactory.create()
        game = games_factories.GameFactory.create()
        game.teams.set((team_1, team_2))

        form = forms.CreatePick(initial={"game": game})

        assert form.is_valid() is False

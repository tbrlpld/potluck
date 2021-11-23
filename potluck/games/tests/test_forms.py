import pytest

from potluck.games.forms import CreateGameInPotForm
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestCreateGame:
    def test_no_pot(self):
        with pytest.raises(TypeError):
            CreateGameInPotForm()

    def test_empty_form(self):
        pot = pots_factories.PotFactory()
        form = CreateGameInPotForm(pot=pot)

        result = form.is_valid()

        assert result is False
        assert form.pot == pot

    def test_with_empty_data(self):
        pot = pots_factories.PotFactory()
        form = CreateGameInPotForm(data={}, pot=pot)

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_empty_teams(self):
        pot = pots_factories.PotFactory()
        form = CreateGameInPotForm({"teams": []}, pot=pot)

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_one_team(self):
        pot = pots_factories.PotFactory()
        team_1 = teams_factories.TeamFactory()
        form = CreateGameInPotForm(data={"teams": [team_1]}, pot=pot)

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_three_teams(self):
        pot = pots_factories.PotFactory()
        team_1 = teams_factories.TeamFactory()
        team_2 = teams_factories.TeamFactory()
        team_3 = teams_factories.TeamFactory()
        form = CreateGameInPotForm(
            data={"teams": [team_1, team_2, team_3]},
            pot=pot,
        )

        result = form.is_valid()

        assert result is False
        assert "teams" in form.errors

    def test_with_two_teams(self):
        pot = pots_factories.PotFactory()
        team_1 = teams_factories.TeamFactory()
        team_2 = teams_factories.TeamFactory()
        form = CreateGameInPotForm(
            data={"teams": [team_1, team_2]},
            pot=pot,
        )

        result = form.is_valid()

        assert result is True
        assert "teams" not in form.errors
        assert "pot" not in form.errors
        game = form.save()
        assert game.pot == pot

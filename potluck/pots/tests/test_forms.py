import pytest

from potluck.pots.forms import CreateGameInPotForm, SetTiebreakerScoreForm
from potluck.pots.tests import factories as pots_factories
from potluck.teams.tests import factories as teams_factories


class TestSetTiebreakerScoreForm:
    def test_is_valid(self):
        form = SetTiebreakerScoreForm({"tiebreaker_score": 1})

        result = form.is_valid()

        assert result is True

    def test_set_value_on_instance(self):
        pot = pots_factories.PotFactory.build()
        form = SetTiebreakerScoreForm({"tiebreaker_score": 1}, instance=pot)
        form.is_valid()

        result = pot.tiebreaker_score

        assert result == 1


@pytest.mark.django_db
class TestCreateGame:
    def test_no_pot(self):
        with pytest.raises(TypeError):
            form = CreateGameInPotForm()

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

import pytest

from potluck.pots.forms import GameAddForm, SetTiebreakerScoreForm
from potluck.pots.tests.factories import PotFactory
from potluck.teams.tests.factories import TeamFactory


class TestSetTiebreakerScoreForm:
    def test_is_valid(self):
        form = SetTiebreakerScoreForm({"tiebreaker_score": 1})

        result = form.is_valid()

        assert result is True

    def test_set_value_on_instance(self):
        pot = PotFactory.build()
        form = SetTiebreakerScoreForm({"tiebreaker_score": 1}, instance=pot)
        form.is_valid()

        result = pot.tiebreaker_score

        assert result == 1


@pytest.mark.django_db
class TestGameAddForm:
    def test_is_valid_raises_error_with_no_team(self):
        form = GameAddForm({"teams": []})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_raises_error_with_one_team(self):
        team_1 = TeamFactory()
        form = GameAddForm({"teams": [team_1]})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_raises_error_with_three_team(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        team_3 = TeamFactory()
        form = GameAddForm({"teams": [team_1, team_2, team_3]})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_success_with_two_team(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        form = GameAddForm({"teams": [team_1, team_2]})

        validation_passed = form.is_valid()

        assert validation_passed is True

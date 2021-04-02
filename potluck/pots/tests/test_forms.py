import pytest

from potluck.pots.forms import AddGameForm
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestAddGameForm:
    def test_is_valid_raises_error_with_no_team(self):
        form = AddGameForm({"teams": []})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_raises_error_with_one_team(self):
        team_1 = TeamFactory()
        form = AddGameForm({"teams": [team_1]})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_raises_error_with_three_team(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        team_3 = TeamFactory()
        form = AddGameForm({"teams": [team_1, team_2, team_3]})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_success_with_two_team(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        form = AddGameForm({"teams": [team_1, team_2]})

        validation_passed = form.is_valid()

        assert validation_passed is True

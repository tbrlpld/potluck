import pytest

from potluck.games.forms import CreateGameForm
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestCreateGameForm:
    def test_is_valid_raises_error_with_no_team(self):
        form = CreateGameForm({"teams": []})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_raises_error_with_one_team(self):
        team_1 = TeamFactory()
        form = CreateGameForm({"teams": [team_1]})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_raises_error_with_three_team(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        team_3 = TeamFactory()
        form = CreateGameForm({"teams": [team_1, team_2, team_3]})

        validation_passed = form.is_valid()

        assert validation_passed is False

    def test_is_valid_success_with_two_team(self):
        team_1 = TeamFactory()
        team_2 = TeamFactory()
        form = CreateGameForm({"teams": [team_1, team_2]})

        validation_passed = form.is_valid()

        assert validation_passed is True

from django.core import exceptions
import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestGame:
    def test_full_clean_validation_error_no_team(self):
        game = GameFactory.create()

        with pytest.raises(exceptions.ValidationError):
            game.full_clean()

    def test_full_clean_validation_error_one_team(self):
        team_1 = TeamFactory.create()
        game = GameFactory.create()
        game.teams.add(team_1)

        with pytest.raises(exceptions.ValidationError):
            game.full_clean()

    def test_full_clean_validation_error_three_teams(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        team_3 = TeamFactory.create()
        game = GameFactory.create()
        game.teams.set([team_1, team_2, team_3])

        with pytest.raises(exceptions.ValidationError):
            game.full_clean()

    def test_full_clean_pass_two_teams(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        game = GameFactory.create()
        game.teams.set([team_1, team_2])

        result = game.full_clean()

        assert result is None

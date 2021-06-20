from django.core import exceptions

import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestGame:
    def test_set_winning_team_saves_to_db(self):
        game = GameFactory.create()
        winning_team = game.teams.first()

        game.set_winning_team(winning_team)

        assert Game.objects.get(pk=game.id).winning_team == winning_team

    def test_set_winning_team_raises_validation_error_if_team_not_in_game(self):
        game = GameFactory.create()
        team_not_in_game = TeamFactory.create()
        assert team_not_in_game not in game.teams.all()

        with pytest.raises(exceptions.ValidationError):
            game.set_winning_team(team_not_in_game)

from django.core import exceptions

import pytest

from potluck.games.models import Game
from potluck.games.tests.factories import GameFactory
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestGame:
    def test_set_winning_team_saves_to_db(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        game = GameFactory.create()
        game.teams.set((team_1, team_2))

        game.set_winning_team(team_1)

        assert Game.objects.get(pk=game.id).winning_team == team_1

    def test_set_winning_team_with_team_not_in_game(self):
        team_1 = TeamFactory.create()
        team_2 = TeamFactory.create()
        team_not_in_game = TeamFactory.create()
        game = GameFactory.create()
        game.teams.set((team_1, team_2))
        assert team_not_in_game not in game.teams.all()

        with pytest.raises(exceptions.ValidationError):
            game.set_winning_team(team_not_in_game)

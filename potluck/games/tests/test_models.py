from django.core import exceptions

import pytest

from potluck.games import models as games_models
from potluck.games.tests import factories as games_factories
from potluck.teams.tests import factories as teams_factories


@pytest.mark.django_db
class TestGame:
    def test_set_winning_team_saves_to_db(self):
        team_1 = teams_factories.TeamFactory.create()
        team_2 = teams_factories.TeamFactory.create()
        game = games_factories.GameFactory.create()
        game.teams.set((team_1, team_2))

        game.set_winning_team(team_1)

        assert games_models.Game.objects.get(pk=game.id).winning_team == team_1

    def test_set_winning_team_with_team_not_in_game(self):
        team_1 = teams_factories.TeamFactory.create()
        team_2 = teams_factories.TeamFactory.create()
        team_not_in_game = teams_factories.TeamFactory.create()
        game = games_factories.GameFactory.create()
        game.teams.set((team_1, team_2))
        assert team_not_in_game not in game.teams.all()

        with pytest.raises(exceptions.ValidationError):
            game.set_winning_team(team_not_in_game)
